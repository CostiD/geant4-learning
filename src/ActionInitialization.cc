#include "ActionInitialization.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"

ActionInitialization::ActionInitialization(DetectorConstruction* det)
    : fDetector(det) {}

void ActionInitialization::BuildForMaster() const
{
    SetUserAction(new RunAction(fDetector));
}

void ActionInitialization::Build() const
{
    auto* eventAct = new EventAction();
    SetUserAction(new PrimaryGeneratorAction());
    SetUserAction(new RunAction(fDetector));
    SetUserAction(eventAct);
    SetUserAction(new SteppingAction(fDetector, eventAct));
}
