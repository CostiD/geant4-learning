#include "EventAction.hh"
#include "RunAction.hh"
#include "G4RunManager.hh"

void EventAction::BeginOfEventAction(const G4Event*)
{
    fEdep     = 0.;
    fStepLen  = 0.;
    fEntryX   = 0.;
    fEntryY   = 0.;
    fEntrySet = false;
}

void EventAction::EndOfEventAction(const G4Event*)
{
    auto* runAction = static_cast<const RunAction*>(
        G4RunManager::GetRunManager()->GetUserRunAction());
    // Cast away const to call FillEvent (non-const method writing to file)
    const_cast<RunAction*>(runAction)->FillEvent(
        fEdep, fStepLen, fEntryX, fEntryY, fEntrySet);
}
