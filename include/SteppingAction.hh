#ifndef SteppingAction_h
#define SteppingAction_h

#include "G4UserSteppingAction.hh"
#include "globals.hh"

class DetectorConstruction;
class EventAction;

class SteppingAction : public G4UserSteppingAction
{
public:
    SteppingAction(const DetectorConstruction* det, EventAction* evt);
    ~SteppingAction() override = default;

    void UserSteppingAction(const G4Step*) override;

private:
    const DetectorConstruction* fDetector;
    EventAction*                fEventAction;
};

#endif
