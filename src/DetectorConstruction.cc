#include "DetectorConstruction.hh"

#include "G4NistManager.hh"
#include "G4Material.hh"
#include "G4Element.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4Colour.hh"
#include "G4UserLimits.hh"

DetectorConstruction::DetectorConstruction() : G4VUserDetectorConstruction() {}

void DetectorConstruction::DefineMaterials()
{
    // CR-39 (poly-allyl-diglycol-carbonate): C12H18O7, rho=1.31 g/cm3
    G4NistManager* nist = G4NistManager::Instance();
    G4Element* C = nist->FindOrBuildElement("C");
    G4Element* H = nist->FindOrBuildElement("H");
    G4Element* O = nist->FindOrBuildElement("O");

    G4Material* CR39 = new G4Material("CR39", 1.31*g/cm3, 3);
    CR39->AddElement(C, 12);
    CR39->AddElement(H, 18);
    CR39->AddElement(O,  7);
}

G4VPhysicalVolume* DetectorConstruction::Construct()
{
    DefineMaterials();
    G4NistManager* nist = G4NistManager::Instance();
    G4Material* air  = nist->FindOrBuildMaterial("G4_AIR");
    G4Material* CR39 = G4Material::GetMaterial("CR39");

    // World: 15×15×15 cm box of air
    G4double worldSize = 15.*cm;
    auto* solidWorld = new G4Box("World", worldSize, worldSize, worldSize);
    auto* logicWorld = new G4LogicalVolume(solidWorld, air, "World");
    auto* physWorld  = new G4PVPlacement(nullptr, G4ThreeVector(), logicWorld,
                                         "World", nullptr, false, 0, true);

    // CR-39 detector slab at z = fDetectorZ (centre of slab)
    auto* solidDet = new G4Box("CR39",
                               fDetSize/2., fDetSize/2., fDetThickness/2.);
    fCR39LogVol = new G4LogicalVolume(solidDet, CR39, "CR39");

    // Fine step limit inside detector for accurate LET scoring
    fCR39LogVol->SetUserLimits(new G4UserLimits(1.*um));

    G4ThreeVector detPos(0., 0., fDetectorZ + fDetThickness/2.);
    new G4PVPlacement(nullptr, detPos, fCR39LogVol, "CR39",
                      logicWorld, false, 0, true);

    // Visualisation
    logicWorld->SetVisAttributes(G4VisAttributes::GetInvisible());

    auto* detVA = new G4VisAttributes(G4Colour(0.2, 0.6, 1.0, 0.5));
    detVA->SetForceSolid(true);
    fCR39LogVol->SetVisAttributes(detVA);

    return physWorld;
}
