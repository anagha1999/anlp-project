# Cross-Cultural Moral Foundations Analysis

This repository contains code and analysis for studying moral foundations across multiple languages using natural language processing techniques. The project implements Moral Foundations Dictionary generation and analysis for English, Tamil, and Kannada languages.

## Repository Structure

### Root Directory

- **ANLP_project.ipynb**: Main project notebook containing comprehensive analysis and experiments.
- **Cross_Cultural_Statistical_Analysis.ipynb**: Statistical analysis comparing moral foundations across different languages and cultures.
- **mfd2.0.dic**: Original Moral Foundations Dictionary version 2.0 used as reference for English language analysis.
- **master_vectors_all_languages.pkl**: Aggregated word embedding vectors across all three languages for cross-linguistic comparison.
- **cross_cultural_*.csv**: Results and summary statistics from cross-cultural comparative analysis.
- **cross_cultural_*.png**: Visualization outputs including heatmaps, rankings, and comparison charts for cross-cultural analysis.

### Language-Specific Directories

#### english/
Contains English language analysis pipeline and outputs.

- **2.English_Text_Preprocessing.ipynb**: Data cleaning and preprocessing for English text corpus.
- **3.English_Moral_Scoring.ipynb**: Moral foundations scoring implementation for English texts.
- **5.Lexicon_Based_Comparison.ipynb**: Comparison between generated moral lexicon and baseline dictionary.
- **english_master_moral_vectors.pkl**: Trained word embeddings for moral foundations in English.
- **dataEnglish/**: Raw English language datasets.
- **processedDataEnglish/**: Cleaned and preprocessed English text data.
- **english-step3-results/**: Output files from moral scoring analysis.
- **lexicon-comparison-results/**: Evaluation metrics comparing lexicon-based approaches.

#### tamil/
Contains Tamil language analysis pipeline and outputs.

- **1a.Generate_Tamil_MFD.ipynb**: Initial approach for generating Tamil Moral Foundations Dictionary.
- **1b.Generate_Tamil_MFD.ipynb**: Alternative approach for generating Tamil Moral Foundations Dictionary.
- **2.Clean_Preprocess_Tamil_Dataset.ipynb**: Data cleaning and preprocessing for Tamil text corpus.
- **3.Moral_Foundations_Tamil.ipynb**: Moral foundations scoring implementation for Tamil texts.
- **4.Eval_MFD.ipynb**: Evaluation of generated Tamil Moral Foundations Dictionary.
- **5.Lexicon_Based_Comparison.ipynb**: Comparison between generated moral lexicon and baseline approaches.
- **5b.Sample_Tamil_Units.ipynb**: Sampling and evaluation of Tamil text units for validation.
- **5b.PoemTamil-Human1Evaluation-Human2EvaluationRanked-Agreement-Notes.csv**: Human evaluation data for Tamil poems with inter-annotator agreement metrics.
- **tamil_mfd.dic**: Generated Moral Foundations Dictionary for Tamil language.
- **tamil_mfd.pkl**: Serialized Tamil MFD data structure.
- **tamil_master_moral_vectors.pkl**: Trained word embeddings for moral foundations in Tamil.
- **tamil_mfd_embeddings.pkl**: Embeddings specifically for Tamil MFD terms.
- **tamil_samples.dic**: Sample Tamil text units for evaluation purposes.
- **tamil_samples.pkl**: Serialized Tamil sample data.
- **tamil-dataset/**: Raw Tamil language datasets.
- **tamil-csv/**: CSV format datasets for Tamil analysis.
- **tamil-step3-results/**: Output files from moral scoring analysis.
- **lexicon-comparison-results/**: Evaluation metrics comparing lexicon-based approaches.

#### kannada/
Contains Kannada language analysis pipeline and outputs.

- **1.Generate_Kannada_MFD.ipynb**: Generation of Kannada Moral Foundations Dictionary.
- **2.Clean_Preprocess_Kannada_Dataset.ipynb**: Data cleaning and preprocessing for Kannada text corpus.
- **3.Moral_Foundations_Kannada.ipynb**: Moral foundations scoring implementation for Kannada texts.
- **4.Eval_MFD.ipynb**: Evaluation of generated Kannada Moral Foundations Dictionary.
- **5a.Eval_Moral_Extraction_Lexicon.ipynb**: Evaluation of moral concept extraction using lexicon-based methods.
- **5b.Para-TextKannada-Human1Evaluation-Human2EvaluationRanked-Agreement-Notes.csv**: Human evaluation data for Kannada paragraphs with inter-annotator agreement metrics.
- **kannada_mfd.dic**: Generated Moral Foundations Dictionary for Kannada language.
- **kannada_mfd.pkl**: Serialized Kannada MFD data structure.
- **kannada_master_moral_vectors.pkl**: Trained word embeddings for moral foundations in Kannada.
- **kannada_mfd_embeddings.pkl**: Embeddings specifically for Kannada MFD terms.
- **kannada_texts_embeddings.pkl**: Embeddings for Kannada text corpus.
- **kannada_samples.dic**: Sample Kannada text units for evaluation purposes.
- **kannada_samples.pkl**: Serialized Kannada sample data.
- **stop-words.txt**: Kannada language stopwords list for text preprocessing.
- **kannada-dataset/**: Raw Kannada language datasets.
- **kannada-csv/**: CSV format datasets for Kannada analysis.
- **kannada-pre-processed/**: Cleaned and preprocessed Kannada text data.
- **kannada-pre-processed-legacy/**: Previous version of preprocessed data retained for reference.
- **debug/**: Debugging outputs and intermediate files for troubleshooting.
- **phase3_outputs/**: Output files from moral scoring analysis phase.
- **lexicon-comparison-results/**: Evaluation metrics comparing lexicon-based approaches.

### Additional Directories

#### latex-resources/
Contains visualization assets for LaTeX document preparation.

- **kannada-mfd-eval.png**: Evaluation visualization for Kannada MFD performance.

#### WIP/
Work-in-progress directory containing experimental code and preliminary analysis. This folder is not part of the active project codebase and should be ignored.

## Workflow

The analysis pipeline follows a consistent structure across all three languages:

1. Generate or adapt Moral Foundations Dictionary for the target language.
2. Clean and preprocess the text corpus.
3. Apply moral foundations scoring to identify moral content in texts.
4. Evaluate the generated dictionary against human annotations.
5. Compare lexicon-based approaches with alternative methods.

Cross-cultural analysis is performed by aggregating results from all three languages and conducting statistical comparisons.

## Data Formats

- **.ipynb**: Jupyter notebooks containing analysis code and documentation.
- **.pkl**: Serialized Python objects storing embeddings and processed data structures.
- **.dic**: Dictionary files mapping words to moral foundations categories.
- **.csv**: Tabular data including evaluation results and human annotations.
- **.png**: Visualization outputs including charts and heatmaps.

## Requirements

This project uses Python with standard data science libraries including pandas, numpy, scikit-learn, and matplotlib. Jupyter notebook environment is required for running analysis notebooks.
