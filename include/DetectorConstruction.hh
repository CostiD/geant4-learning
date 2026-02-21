#ifndef DetectorConstruction_h
#define DetectorConstruction_h

#include "G4VUserDetectorConstruction.hh"
#include "G4LogicalVolume.hh"
#include "globals.hh"

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    DetectorConstruction();
    ~DetectorConstruction() override = default;

    G4VPhysicalVolume* Construct() override;

    G4LogicalVolume* GetCR39LogVol() const { return fCR39LogVol; }
    G4double         GetDetectorZ()  const { return fDetectorZ;  }
    G4double         GetDetThickness() const { return fDetThickness; }

private:
    void DefineMaterials();

    G4LogicalVolume* fCR39LogVol = nullptr;
    G4double fDetectorZ    = 3.0 * CLHEP::cm;   // distance from beam exit
    G4double fDetThickness = 0.5 * CLHEP::mm;    // standard CR-39 foil
    G4double fDetSize      = 3.0 * CLHEP::cm;    // 3×3 cm active area
};

#endif
