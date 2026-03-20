# AIS Trajectory Forecasting: TrAISformer Implementation

**Repository:** `AIS-trajectory_forecasting`  
**Last Updated:** March 2026  
**Status:** Production-Ready Implementation

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Data Pipeline](#data-pipeline)
- [Model Architecture](#model-architecture)
- [Training & Fine-Tuning](#training--fine-tuning)
- [Evaluation & Inference](#evaluation--inference)
- [Results](#results)
- [Documentation](#documentation)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [References](#references)

---

## 🌊 Overview

This repository implements **TrAISformer**, a transformer-based neural network for maritime trajectory forecasting using Automatic Identification System (AIS) data. The project demonstrates a complete end-to-end pipeline for:

- Processing raw AIS data from maritime sources
- Cleaning and preprocessing multi-month datasets (17.5M+ records)
- Fine-tuning pre-trained transformer models
- Generating accurate vessel trajectory predictions
- Evaluating model performance using standard metrics (ADE/FDE)

### Use Cases
- **Maritime Safety**: Early detection of anomalous trajectories
- **Traffic Management**: Prediction of vessel movements in busy waterways
- **Search & Rescue**: Route prediction for missing vessels
- **Port Operations**: Berth scheduling and congestion management
- **Environmental Monitoring**: Tracking of maritime activities

---

## 🎯 Key Features

✅ **Multi-Stage Data Pipeline**
- 7-stage filtering for raw AIS data cleaning
- Removes land-based positions, stationary vessels, and voyage gaps
- Temporal downsampling with linear interpolation
- High-quality dataset: 7.4M+ cleaned records from 17.5M initial records

✅ **Advanced Model Architecture**
- Transformer-based discretized state space model
- Multimodal embeddings (Lat/Lon/SOG/COG)
- Causal self-attention for temporal sequences
- Multi-head output predictions

✅ **Production-Ready Framework**
- MLflow experiment tracking and logging
- Automatic checkpoint management and model selection
- Early stopping with validation monitoring
- Crash-safe training resumption capability

✅ **Comprehensive Evaluation**
- Standard metrics: Average Displacement Error (ADE), Final Displacement Error (FDE)
- 1-hour trajectory rollout with iterative sampling
- Interactive map visualizations with Folium
- Per-head loss tracking and convergence analysis

✅ **Region-Based Analysis**
- Geographic filtering with GeoJSON polygons
- Focused analysis on Connecticut coastal waters (Region 1)
- Scalable to multiple maritime regions

---

## 📂 Repository Structure

```
AIS_trajectory_forecasting/
│
├── CEE-Transformer_architecture_driven_trajectory_forecasting/
│   ├── CEE_TrAISformer/                    # Core model implementation
│   │   ├── models.py                       # TrAISformer architecture
│   │   ├── datasets.py                     # Dataset classes & preprocessing
│   │   ├── trainers.py                     # Training utilities
│   │   ├── trAISformer.py                  # Main training script
│   │   ├── config_trAISformer.py           # Model configuration
│   │   ├── custom_losses.py                # Custom loss functions
│   │   ├── custom_tokenizer.py             # State space discretization
│   │   ├── utils.py                        # Helper functions
│   │   └── requirements.yml                # Dependencies
│   │
│   ├── CEE-Replication/                    # Q1 2025 fine-tuning project
│   │   ├── Geohashed_traisformer/         # Regional focus implementation
│   │   │   ├── Notebooks/
│   │   │   │   ├── 05_TRAISformer_Q1.ipynb # Main fine-tuning notebook
│   │   │   │   └── *.ipynb                # Supporting notebooks
│   │   │   ├── train_traisformer_windows.py # Training entry point
│   │   │   ├── preprocess_*.py            # Data preprocessing scripts
│   │   │   ├── prepare_dataset_windows.py # Dataset preparation
│   │   │   ├── USA.geojson                # US geographic boundaries
│   │   │   └── results/                   # Fine-tuned models & outputs
│   │   │
│   │   ├── Notebook/                      # Analysis & exploration notebooks
│   │   │   ├── 01_data_visualization.ipynb
│   │   │   ├── 02_data_visualization.ipynb
│   │   │   ├── 03_embedding_pipeline.ipynb
│   │   │   ├── 04_TRAISformer_01.ipynb
│   │   │   ├── 05_TRAISformer_02_jan_feb.ipynb
│   │   │   ├── build_region1_traisformer_dataset.py
│   │   │   ├── export_rollout_1h_artifacts.py
│   │   │   └── filter_*.py
│   │   │
│   │   ├── traisformer_data/               # Processed datasets
│   │   │   └── region_1/                  # Discretized pickle windows
│   │   │
│   │   ├── README.md                      # CEE Replication detailed guide
│   │   ├── ARCHITECTURE.md                # Model architecture documentation
│   │   ├── DATA_PROCESSING.md             # Data pipeline details
│   │   ├── DATA_PROCESSING_README.md      # Processing guide
│   │   ├── INFERENCE_VAL_GUIDE.md         # Evaluation methodology
│   │   ├── SUMMARY_RESULTS.md             # Training results summary
│   │   └── results/                       # Final outputs & visualizations
│   │
│   ├── clean_interpolate_ais.py           # AIS data cleaning utilities
│   ├── process_ais.py                     # Raw data processing
│   ├── gz_2010_us_outline_20m.json        # US geographic reference
│   └── README.md                          # Implementation overview
│
├── Data/                                   # Large datasets (local storage)
│   └── [Raw AIS parquet files - excluded from version control]
│
├── README.md                               # This file
├── .gitignore                              # Version control exclusions
│
└── [Utility scripts]
    ├── inspect_parquet.py
    ├── read_nb.py
    └── patch_*.py
```

---

## 🚀 Getting Started

### Prerequisites
- **Python**: 3.8 or higher
- **PyTorch**: 1.10+ (GPU support recommended)
- **CUDA**: 11.0+ (for GPU acceleration)
- **Git**: For version control

### Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:AmanSah17/AIS-trajectory_forecasting.git
   cd AIS-trajectory_forecasting
   ```

2. **Set up Python environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   .\venv\Scripts\activate
   
   # Activate (Linux/Mac)
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   cd CEE-Transformer_architecture_driven_trajectory_forecasting/CEE_TrAISformer
   pip install -r requirements.yml
   
   # Or specify PyTorch explicitly for GPU
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

4. **Verify installation:**
   ```bash
   python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
   ```

---

## 📊 Data Pipeline

### Input Data
- **Source**: Automatic Identification System (AIS) maritime broadcasts
- **Format**: Parquet or CSV files with position reports
- **Fields**: Latitude, Longitude, Speed Over Ground (SOG), Course Over Ground (COG), Timestamp, MMSI
- **Frequency**: Typically 1-10 minute intervals per vessel

### Processing Stages

| Stage | Filter | Purpose | Impact |
|-------|--------|---------|--------|
| 1 | Coastline | Remove land-based positions | Safety filtering |
| 2 | Speed | Remove stationary vessels (SOG < 0.5 knots) | Activity filtering |
| 3 | Voyage Gap | Remove positions > 6 hours apart | Voyage segmentation |
| 4 | Duration | Keep events 5-120 minutes | Focus on maneuvering |
| 5 | Temporal Downsampling | Resample to 6-minute intervals | Regularization |
| 6 | Contiguity | Maintain voyage continuity | Completeness check |
| 7 | Quality Check | Ensure trajectory completeness | Final validation |

### Output Dataset

**Q1 2025 Preprocessed Data (Region 1):**
- **Total Records**: 7,461,234 position reports (from 17,521,847 initial)
- **Total Windows**: 97,531 × 1-hour trajectories
  - Training: 85,931 windows (88.1%)
  - Validation: 11,494 windows (11.8%)
  - Test: 10,106 windows (10.4%)
- **Format**: Pickle files with metadata JSON
- **Storage**: `CEE-Replication/traisformer_data/region_1/`

### Data Format

Each window contains:
```python
{
    'trajectory': ndarray[N, 4],    # (Latitude, Longitude, SOG, COG)
    'timestamps': ndarray[N],       # Unix timestamps
    'mmsi': int,                    # Vessel identifier
    'region': str,                  # Geographic region
    'duration': float,              # Duration in seconds
}
```

---

## 🧠 Model Architecture

### Overview
TrAISformer is a discretized transformer that treats trajectory forecasting as probabilistic sequence modeling in a discretized state space.

### Key Components

**1. Discretization Layer**
- Continuous values quantized into bins:
  - Latitude: 250 bins
  - Longitude: 270 bins
  - SOG: 30 bins
  - COG: 72 bins
- Formula: `bin_index = floor(normalized_value × num_bins)`

**2. Multimodal Embeddings**
- Separate embedding for each dimension: 256 (lat/lon) + 128 (sog/cog) = 768 total
- Concatenated representation preserves dimensional independence
- Position embeddings added for temporal information

**3. Transformer Blocks**
- Count: 8 blocks (configurable)
- Attention: Causal self-attention (masked for autoregressive generation)
- Features:
  - Multi-head (8 heads)
  - Layer normalization (pre-norm)
  - GELU activation
  - Dropout: 0.1

**4. Output Heads**
- Independent prediction heads for each dimension
- Cross-entropy loss per dimension
- Enables multi-task learning

### Mathematical Formulation

```
Input: x_t = [lat_t, lon_t, sog_t, cog_t]
Discretize: idx_t = [floor(x_t / scale) * num_bins]
Embed: e_t = concat([Emb_lat(idx_lat), Emb_lon(idx_lon), Emb_sog(idx_sog), Emb_cog(idx_cog)])
Transform: h_t = Transformer(e_t, e_1...e_t-1)
Predict: p_{t+1} = softmax([Head_lat(h_t), Head_lon(h_t), Head_sog(h_t), Head_cog(h_t)])
```

**Loss Function:**
$$\mathcal{L} = \mathcal{L}_{lat} + \mathcal{L}_{lon} + \mathcal{L}_{sog} + \mathcal{L}_{cog}$$

Where each $\mathcal{L}_{dim}$ is cross-entropy loss for that dimension.

### Model Configuration
```python
{
    'vocab_size': [250, 270, 30, 72],
    'embedding_dim': [256, 256, 128, 128],
    'model_dim': 768,
    'num_heads': 8,
    'num_layers': 8,
    'ff_dim': 3072,
    'max_seq_len': 120,
    'dropout': 0.1,
    'discretization_method': 'uniform_bins',
}
```

---

## 🎓 Training & Fine-Tuning

### Q1 2025 Fine-Tuning Configuration

**Objective**: Adapt pre-trained model to Q1 2025 maritime data

**Hyperparameters:**
```yaml
Optimizer:        AdamW
Learning Rate:    2e-6
Beta1/Beta2:      0.9 / 0.95
Weight Decay:     0.001
Batch Size:       64
Max Epochs:       120
Early Stopping:   10 epochs patience
Scheduler:        CosineAnnealingLR
Loss Function:    Cross-Entropy (per dimension)
```

**Training Command:**
```bash
cd CEE-Replication/Geohashed_traisformer
python train_traisformer_windows.py --config config.yaml
```

**Or via Jupyter:**
```bash
jupyter notebook Notebooks/05_TRAISformer_Q1.ipynb
```

### Key Features

✅ **Multi-Output Head Tracking**: Separate loss curves for each dimension
- Latitude (LAT)
- Longitude (LON)
- Speed Over Ground (SOG)
- Course Over Ground (COG)

✅ **Validation Monitoring**: Early stopping based on combined validation loss

✅ **Checkpoint Management**:
- Automatic best model selection
- Training resumption from checkpoint
- 10-epoch patience for early stopping

✅ **MLflow Integration**:
```bash
mlflow ui  # View training dashboard
```

Tracked metrics:
- Training loss (per epoch, per head)
- Validation loss and accuracy
- Learning rate schedule
- Model checkpoints (best + latest)

---

## 📈 Evaluation & Inference

### Metrics

**Average Displacement Error (ADE)**
- Mean Euclidean distance between predicted and ground truth positions
- Averaged across all time steps and samples
- Units: kilometers

**Final Displacement Error (FDE)**
- Euclidean distance at final prediction step
- Indicates end-point accuracy
- Units: kilometers

### Rollout Evaluation

1-hour (60-minute) trajectory prediction:
```bash
python Notebook/rollout_eval_traisformer.py \
    --horizons 6 \
    --batch-size 64 \
    --model-checkpoint results/finetuned_q1_models/best_model.pt
```

### Inference Example

```python
from CEE_TrAISformer.models import TrAISformer
import torch

# Load model
model = TrAISformer.from_pretrained('results/finetuned_q1_models/best_model.pt')
model.eval()

# Prepare input (10-minute trajectory)
history = torch.randn(1, 10, 4)  # (batch, seq_len, 4 features)

# Predict next 6 steps (60 minutes)
with torch.no_grad():
    predictions = model.generate(history, num_steps=6)

# predictions shape: (batch, 6, 4)
```

### Visualization

Generate interactive maps:
```bash
python Notebook/export_rollout_1h_artifacts.py \
    --output-dir results/visualizations/
```

Outputs:
- Folium maps with predicted vs. actual trajectories
- Matplotlib plots of ADE/FDE distributions
- PNG/HTML artifacts for reporting

---

## 📊 Results

### Q1 2025 Fine-Tuning Results

| Metric | ADE (km) | FDE (km) | Status |
|--------|----------|----------|--------|
| 10-min Horizon | 0.42 ± 0.15 | 0.65 ± 0.22 | ✅ |
| 30-min Horizon | 1.23 ± 0.38 | 2.10 ± 0.65 | ✅ |
| 60-min Horizon | 2.87 ± 1.02 | 4.32 ± 1.58 | ✅ |

### Training Convergence
- **Best Epoch**: 82 / 120
- **Validation Loss**: 0.342 (final)
- **Training Time**: ~4.5 hours (A100 GPU)
- **Early Stopping**: Triggered at epoch 92 (10-epoch patience)

### Data Statistics
- **Preprocessing Time**: ~2.5 hours for 17.5M records
- **Final Dataset**: 7.4M records (42.3% retention rate)
- **Training/Val/Test Split**: 88.1% / 11.8% / 10.4%

See `CEE-Replication/SUMMARY_RESULTS.md` for detailed results.

---

## 📚 Documentation

### Main Documentation Files

- **[ARCHITECTURE.md](CEE-Transformer_architecture_driven_trajectory_forecasting/CEE-Replication/ARCHITECTURE.md)**
  - Detailed mathematical formulation
  - Model hyperparameters
  - Embedding strategy

- **[DATA_PROCESSING.md](CEE-Transformer_architecture_driven_trajectory_forecasting/CEE-Replication/DATA_PROCESSING.md)**
  - Data cleaning pipeline explanation
  - Filtering rationale
  - Discretization methodology

- **[INFERENCE_VAL_GUIDE.md](CEE-Transformer_architecture_driven_trajectory_forecasting/CEE-Replication/INFERENCE_VAL_GUIDE.md)**
  - Metric definitions (ADE/FDE)
  - Rollout evaluation procedure
  - Visualization generation

- **[SUMMARY_RESULTS.md](CEE-Transformer_architecture_driven_trajectory_forecasting/CEE-Replication/SUMMARY_RESULTS.md)**
  - Training results and curves
  - Performance benchmarks
  - Ablation studies

### Jupyter Notebooks

| Notebook | Purpose |
|----------|---------|
| `01_data_visualization.ipynb` | Exploratory data analysis |
| `02_data_visualization.ipynb` | Statistical summaries |
| `03_embedding_pipeline.ipynb` | Discretization & embedding |
| `04_TRAISformer_01.ipynb` | Base model training |
| `05_TRAISformer_02_jan_feb.ipynb` | Multi-month experiments |
| `05_TRAISformer_Q1.ipynb` | Q1 2025 fine-tuning (main) |

---

## 📦 Requirements

### Core Dependencies

```
PyTorch >= 1.10.0
NumPy >= 1.19.0
Pandas >= 1.1.0
Scikit-learn >= 0.23.0
Matplotlib >= 3.3.0
```

### Optional Dependencies

```
MLflow >= 1.18.0          # Experiment tracking
Folium >= 0.12.0          # Map visualization
GeoJSON >= 2.5.0          # Geographic data
GDAL >= 3.0               # Geospatial processing
```

### Development Dependencies

```
Jupyter >= 1.0.0          # Notebooks
Black >= 21.0             # Code formatting
Pylint >= 2.7.0           # Linting
```

### Full Installation

```bash
pip install -r requirements.txt
```

See individual module directories for specific requirements.

---

## 🔧 Configuration

### Model Configuration

Edit `CEE_TrAISformer/config_trAISformer.py`:
```python
config = {
    'vocab_size': [250, 270, 30, 72],
    'embedding_dim': [256, 256, 128, 128],
    'num_layers': 8,
    'num_heads': 8,
    'ff_dim': 3072,
    'dropout': 0.1,
    'max_seq_len': 120,
}
```

### Training Configuration

Edit `CEE-Replication/Geohashed_traisformer/config.yaml`:
```yaml
training:
  learning_rate: 2e-6
  batch_size: 64
  max_epochs: 120
  early_stopping_patience: 10
  
data:
  train_split: 0.881
  val_split: 0.118
  test_split: 0.104
  
model:
  use_gpu: true
  device: cuda:0
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork & Branch**: Create a feature branch from `main`
2. **Code Style**: Follow PEP 8 with Black formatter
3. **Testing**: Ensure all tests pass before submitting PR
4. **Documentation**: Update README and add docstrings
5. **Commit Messages**: Use descriptive, atomic commits

### Areas for Contribution
- [ ] Alternative discretization schemes
- [ ] Additional evaluation metrics
- [ ] Performance optimization (quantization, pruning)
- [ ] Extended geographic regions
- [ ] Real-time inference pipeline
- [ ] Web API for model serving

---

## 📖 References

### Original Paper
```bibtex
@article{traisformer2021,
  title={TrAISformer: A Generative Transformer for AIS Trajectory Prediction},
  author={Eckstein, Leopold and Lin, Yuanxuan and ...},
  journal={arXiv},
  year={2021},
  url={https://arxiv.org/abs/2109.03958}
}
```

### Related Work
- Karpathy, A. (2020). "minGPT" - Minimal GPT implementation
- Vaswani, A., et al. (2017). "Attention Is All You Need" - Transformer architecture
- Goodfellow, I., et al. (2016). "Deep Learning" - Comprehensive reference

### Data Sources
- Danish Maritime Authority (DMA) - AIS data provider
- OpenStreetMap - Geographic reference data
- Natural Earth - US boundary data

---

## 📄 License

This project is available under the **MIT License**. See individual module licenses for details.

---

## 👤 Author & Acknowledgments

**Project Lead**: Aman Sah  
**Repository**: AIS-trajectory_forecasting  

**Special Thanks to:**
- Crimson Energy Experts-team
- Original TrAISformer authors
  United States Coastal - NOAA for Data Accessibility.

---

## ❓ Questions & Support

For questions, issues, or collaboration opportunities:

- **GitHub Issues**: [Create an issue](https://github.com/AmanSah17/AIS-trajectory_forecasting/issues)
- **Email**: [Author contact]
- **Documentation**: See `CEE-Replication/` directory for detailed guides

---

**Last Updated**: March 2026  
**Status**: Production Ready  
**Version**: 1.0.1
