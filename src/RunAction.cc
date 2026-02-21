#include "RunAction.hh"
#include "G4AnalysisManager.hh"
#include "G4Run.hh"
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"
#include "G4Threading.hh"

RunAction::RunAction(DetectorConstruction* det) : fDetector(det) {}

RunAction::~RunAction() {}

void RunAction::BeginOfRunAction(const G4Run*)
{
    auto* mgr = G4AnalysisManager::Instance();
    mgr->SetDefaultFileType("csv");
    mgr->SetVerboseLevel(0);
    mgr->SetNtupleMerging(true);   // merge all threads into one file

    mgr->CreateNtuple("CR39", "Proton hits in CR-39");
    mgr->CreateNtupleIColumn("EventID");      // col 0
    mgr->CreateNtupleDColumn("Edep_MeV");     // col 1
    mgr->CreateNtupleDColumn("TrackLen_mm");  // col 2
    mgr->CreateNtupleDColumn("LET_MeV_mm");  // col 3
    mgr->CreateNtupleDColumn("EntryX_mm");   // col 4
    mgr->CreateNtupleDColumn("EntryY_mm");   // col 5
    mgr->CreateNtupleIColumn("Hit");          // col 6
    mgr->FinishNtuple();

    mgr->OpenFile("cr39_output");
}

void RunAction::EndOfRunAction(const G4Run* run)
{
    auto* mgr = G4AnalysisManager::Instance();
    mgr->Write();
    mgr->CloseFile();

    if (G4Threading::IsMasterThread()) {
        G4int n = run->GetNumberOfEvent();
        G4cout << "\n=== Run Summary ===\n"
               << "Total events : " << n << "\n"
               << "Output       : cr39_output.csv\n"
               << "===================\n" << G4endl;
    }
}

void RunAction::FillEvent(G4double edep, G4double trackLen,
                          G4double x, G4double y, G4bool hit)
{
    static G4Mutex mutex = G4MUTEX_INITIALIZER;
    static G4int evtID = 0;

    G4double let = (trackLen > 0.) ? edep / trackLen : 0.;

    auto* mgr = G4AnalysisManager::Instance();

    G4AutoLock lock(&mutex);
    G4int id = evtID++;
    lock.unlock();  // unlock before filling (mgr is thread-local per ntuple row)

    mgr->FillNtupleIColumn(0, id);
    mgr->FillNtupleDColumn(1, edep / MeV);
    mgr->FillNtupleDColumn(2, trackLen / mm);
    mgr->FillNtupleDColumn(3, let / (MeV/mm));
    mgr->FillNtupleDColumn(4, x / mm);
    mgr->FillNtupleDColumn(5, y / mm);
    mgr->FillNtupleIColumn(6, hit ? 1 : 0);
    mgr->AddNtupleRow();
}
