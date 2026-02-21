//=============================================================================
// CR-39 Proton Irradiation Simulation
// 2.5 MeV protons, detector at 3 cm from beam exit
// Author: PhD candidate simulation — GEANT4 11.1 MT
//=============================================================================

#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "FTFP_BERT.hh"
#include "G4EmStandardPhysics_option4.hh"
#include "G4StepLimiterPhysics.hh"

#include "DetectorConstruction.hh"
#include "ActionInitialization.hh"

int main(int argc, char** argv)
{
    G4UIExecutive* ui = nullptr;
    if (argc == 1) ui = new G4UIExecutive(argc, argv);

    auto* runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::Default);

    auto* physicsList = new FTFP_BERT;
    physicsList->ReplacePhysics(new G4EmStandardPhysics_option4());
    physicsList->RegisterPhysics(new G4StepLimiterPhysics());

    auto* detector = new DetectorConstruction();
    runManager->SetUserInitialization(detector);
    runManager->SetUserInitialization(physicsList);
    runManager->SetUserInitialization(new ActionInitialization(detector));

    G4VisManager* visManager = new G4VisExecutive;
    visManager->Initialize();

    G4UImanager* UImanager = G4UImanager::GetUIpointer();

    if (argc > 1) {
        UImanager->ApplyCommand(G4String("/control/execute ") + argv[1]);
    } else {
        UImanager->ApplyCommand("/control/execute init_vis.mac");
        ui->SessionStart();
        delete ui;
    }

    delete visManager;
    delete runManager;
    return 0;
}
