#include "RunAction.hh"
#include "DetectorConstruction.hh"
#include "EventAction.hh"

#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"
#include <iostream>

RunAction::RunAction(DetectorConstruction* det) : fDetector(det) {}

RunAction::~RunAction() {}

void RunAction::BeginOfRunAction(const G4Run*)
{
    fOutFile.open("cr39_output.csv");
    // LET in MeV/mm, Edep in MeV, track length in mm, position in mm
    fOutFile << "EventID,Edep_MeV,TrackLen_mm,LET_MeV_mm,EntryX_mm,EntryY_mm,Hit\n";
}

void RunAction::EndOfRunAction(const G4Run* run)
{
    fOutFile.close();

    G4int nEvents = run->GetNumberOfEvent();
    G4cout << "\n=== Run Summary ===\n"
           << "Total events: " << nEvents << "\n"
           << "Output: cr39_output.csv\n"
           << "===================\n" << G4endl;
}

void RunAction::FillEvent(G4double edep, G4double trackLen,
                          G4double x, G4double y, G4bool hit)
{
    static G4int evtID = 0;
    G4double let = (trackLen > 0.) ? edep / trackLen : 0.;

    fOutFile << evtID++           << ","
             << edep/MeV          << ","
             << trackLen/mm       << ","
             << let/(MeV/mm)      << ","
             << x/mm              << ","
             << y/mm              << ","
             << (hit ? 1 : 0)     << "\n";
}
