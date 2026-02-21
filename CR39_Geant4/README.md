# CR-39 Proton Irradiation — GEANT4 Simulation

**2.5 MeV proton beam · CR-39 nuclear track detector at 3 cm · GEANT4 11**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/CR39_Geant4/blob/main/CR39_Colab.ipynb)

---

## Physics

| Parameter | Value |
|-----------|-------|
| Particle | Proton |
| Beam energy | 2.5 MeV |
| Beam profile | Gaussian σ = 1 mm |
| Air gap | 3 cm |
| Detector material | CR-39 (C₁₂H₁₈O₇, ρ = 1.31 g/cm³) |
| Detector thickness | 0.5 mm |
| Physics list | FTFP\_BERT + EmStdOpt4 |
| Step limit in CR-39 | 1 µm |

## Project Structure

```
CR39_Geant4/
├── CMakeLists.txt
├── main.cc
├── run.mac               ← batch: 50 000 events
├── init_vis.mac          ← interactive OpenGL
├── include/
│   ├── DetectorConstruction.hh
│   ├── PrimaryGeneratorAction.hh
│   ├── EventAction.hh
│   ├── SteppingAction.hh
│   └── RunAction.hh
├── src/
│   ├── DetectorConstruction.cc
│   ├── PrimaryGeneratorAction.cc
│   ├── EventAction.cc
│   ├── SteppingAction.cc
│   └── RunAction.cc
├── analysis/
│   └── visualize.py      ← publication figures (PDF + PNG)
└── CR39_Colab.ipynb      ← end-to-end Google Colab notebook
```

## Output (`cr39_output.csv`)

| Column | Unit | Description |
|--------|------|-------------|
| EventID | — | Event number |
| Edep\_MeV | MeV | Energy deposited in CR-39 |
| TrackLen\_mm | mm | Proton track length inside CR-39 |
| LET\_MeV\_mm | MeV/mm | Linear energy transfer |
| EntryX\_mm | mm | Hit x-position on detector |
| EntryY\_mm | mm | Hit y-position on detector |
| Hit | 0/1 | Did the proton reach the detector? |

## Running Locally

```bash
git clone https://github.com/YOUR_USERNAME/CR39_Geant4.git
mkdir build && cd build
cmake ../CR39_Geant4 -DGeant4_DIR=/path/to/geant4/lib/Geant4-11.1/
make -j$(nproc)
./CR39_sim run.mac            # batch
./CR39_sim                    # interactive
cd ..
python analysis/visualize.py  # figures
```

## Citation

If you use this simulation, please cite the GEANT4 toolkit:
> S. Agostinelli et al., *Nucl. Instr. Meth. A* **506** (2003) 250–303.
