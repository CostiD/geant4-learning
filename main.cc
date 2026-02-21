//=============================================================================
// CR-39 Proton Irradiation Simulation
// 2.5 MeV protons, detector at 3 cm from beam exit
// Author: PhD candidate simulation — GEANT4 10.7+
//=============================================================================

#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "FTFP_BERT.hh"
#include "G4EmStandardPhysics_option4.hh"
#include "G4StepLimiterPhysics.hh"

#include "DetectorConstruction.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"

int main(int argc, char** argv)
{
    G4UIExecutive* ui = nullptr;
    if (argc == 1) ui = new G4UIExecutive(argc, argv);

    auto* runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Default);

    // Physics: FTFP_BERT with high-precision EM option 4 for low-energy ions
    auto physicsList = new FTFP_BERT;
    physicsList->ReplacePhysics(new G4EmStandardPhysics_option4());
    physicsList->RegisterPhysics(new G4StepLimiterPhysics());

    auto* detector  = new DetectorConstruction();
    auto* eventAct  = new EventAction();

    runManager->SetUserInitialization(detector);
    runManager->SetUserInitialization(physicsList);
    runManager->SetUserAction(new PrimaryGeneratorAction());
    runManager->SetUserAction(new RunAction(detector));
    runManager->SetUserAction(eventAct);
    runManager->SetUserAction(new SteppingAction(detector, eventAct));

    G4VisManager* visManager = new G4VisExecutive;
    visManager->Initialize();

    G4UImanager* UImanager = G4UImanager::GetUIpointer();

    if (argc > 1) {
        G4String command = "/control/execute ";
        UImanager->ApplyCommand(command + argv[1]);
    } else {
        UImanager->ApplyCommand("/control/execute init_vis.mac");
        ui->SessionStart();
        delete ui;
    }

    delete visManager;
    delete runManager;
    return 0;
}
