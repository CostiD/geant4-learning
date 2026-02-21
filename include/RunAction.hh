#ifndef RunAction_h
#define RunAction_h

#include "G4UserRunAction.hh"
#include "globals.hh"

class DetectorConstruction;
class G4Run;

class RunAction : public G4UserRunAction
{
public:
    RunAction(DetectorConstruction* det);
    ~RunAction() override;

    void BeginOfRunAction(const G4Run*) override;
    void EndOfRunAction(const G4Run*) override;

    void FillEvent(G4double edep, G4double trackLen,
                   G4double x, G4double y, G4bool hit);

private:
    DetectorConstruction* fDetector;
};

#endif
