#include "PrimaryGeneratorAction.hh"
#include "G4ParticleTable.hh"
#include "G4SystemOfUnits.hh"
#include "G4Event.hh"
#include "Randomize.hh"

PrimaryGeneratorAction::PrimaryGeneratorAction()
{
    fParticleGun = new G4ParticleGun(1);

    G4ParticleTable* pTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition* proton = pTable->FindParticle("proton");

    fParticleGun->SetParticleDefinition(proton);
    fParticleGun->SetParticleEnergy(2.5 * MeV);
    fParticleGun->SetParticleMomentumDirection(G4ThreeVector(0., 0., 1.));
}

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
    delete fParticleGun;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* event)
{
    // Pencil beam with 1 mm Gaussian divergence (realistic cyclotron beam)
    G4double sigma = 1.0 * mm;
    G4double x0 = G4RandGauss::shoot(0., sigma);
    G4double y0 = G4RandGauss::shoot(0., sigma);

    fParticleGun->SetParticlePosition(G4ThreeVector(x0, y0, -5.*cm));
    fParticleGun->GeneratePrimaryVertex(event);
}
