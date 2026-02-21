#include "SteppingAction.hh"
#include "DetectorConstruction.hh"
#include "EventAction.hh"

#include "G4Step.hh"
#include "G4SystemOfUnits.hh"

SteppingAction::SteppingAction(const DetectorConstruction* det,
                               EventAction* evt)
    : fDetector(det), fEventAction(evt) {}

void SteppingAction::UserSteppingAction(const G4Step* step)
{
    // Score only inside the CR-39 volume
    G4LogicalVolume* volume =
        step->GetPreStepPoint()->GetTouchableHandle()
            ->GetVolume()->GetLogicalVolume();

    if (volume != fDetector->GetCR39LogVol()) return;

    G4double edep    = step->GetTotalEnergyDeposit();
    G4double stepLen = step->GetStepLength();

    fEventAction->AddEdep(edep);
    fEventAction->AddStep(stepLen);

    // Record first hit position (entry point in detector)
    G4ThreeVector pos = step->GetPreStepPoint()->GetPosition();
    fEventAction->SetEntryXY(pos.x(), pos.y());
}
