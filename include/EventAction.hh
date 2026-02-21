#ifndef EventAction_h
#define EventAction_h

#include "G4UserEventAction.hh"
#include "globals.hh"

class EventAction : public G4UserEventAction
{
public:
    EventAction() = default;
    ~EventAction() override = default;

    void BeginOfEventAction(const G4Event*) override;
    void EndOfEventAction(const G4Event*) override;

    void AddEdep(G4double edep)  { fEdep += edep; }
    void AddStep(G4double step)  { fStepLen += step; }
    void SetEntryXY(G4double x, G4double y) {
        if (!fEntrySet) { fEntryX = x; fEntryY = y; fEntrySet = true; }
    }

    G4double GetEdep()   const { return fEdep; }
    G4double GetStepLen() const { return fStepLen; }
    G4double GetEntryX() const { return fEntryX; }
    G4double GetEntryY() const { return fEntryY; }
    G4bool   EntrySet()  const { return fEntrySet; }

private:
    G4double fEdep    = 0.;
    G4double fStepLen = 0.;
    G4double fEntryX  = 0.;
    G4double fEntryY  = 0.;
    G4bool   fEntrySet = false;
};

#endif
