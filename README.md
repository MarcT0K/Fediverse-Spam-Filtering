# Fediverse Spam Filtering

This repo presents a spam filtering for Fediverse social media platforms. For now, the current version is only a proof of concept. 

## Spam filtering model

For spam filtering, we use a Naive Bayes model. This simple approach is classic for email spam filtering and was recently imported to the Fediverse in Pixelfed.
We intend to generalize this approach and provide more features (e.g., decentralized learning). 

## Model training

Spam filters are continually trained. Indeed, the spam filter integrates new (training) data over time to improve its performances. However, a major challenge in Machine Learning is to obtain "annotated" data: for spam filters, a list of statuses with their respective type (spam or ham).

Our system gathers training data in three ways:

1. The administrator can submit some annotated data (e.g., public dataset).
2. The system identifies outliers (i.e., statuses containing many unknown words) and asks the administrator to manually label them => This approach enables enriching the training data in a targeted manner.
3. The system randomly picks some statuses submitted to the spam filtering and asks the administrator to manually label them => This approach verifies that the filter remains in line with the administrator's expectations.

This assisted data annotation minimizes the administrator's workload, while enriching the filtering quality. 

## Feature extraction

The spam filter takes a JSON status as input. We extract various features from this JSON: words from the content, words from the spoiler text, presence of media attachments, tags, and sensitiveness. The goal is to provide as much information as possible to the filtering model. Thus, the feature extraction could be improve to extract even more information from the JSON data. The current implementation demonstrates that our spam filtering can exploit intelligently different elements from the JSON statuses.

## Endpoints

The API provides the following endpoints:

 - [POST] "/filter": predicts whether a status is a spam or not.
 - [GET] "/outliers": returns the list of outliers identified spam filtering (waiting for a manual decision).
 - [POST] "/outliers/classify": receives manual decisions for previously identified outliers.
 - [GET] "/random_checks/": returns a list of randomly selected statuses requiring a manual check.
 - [POST] "/random_checks/": receives manual decisions for randomly selected statuses.
 - [POST] "/training_data/import": update the spam filtering model based on imported data.
 - [GET] "/model/import"
 - [POST] "/model/export"


## Data storage

Our spam filter only uses an embedded key-value store. We create three tables: one for the model parameters, one for the outliers, and one for the randomly picked statuses.

We do not store training data to minimize storage overhead.

## Extensions

Based on this PoC, two directions are possible:

1. Refine this Python implementation to improve its performances and quality (see `TODO.md`)
2. Reimplement this design in Rust to maximize the performances

The first option would simplify the implementation work and could motivate more external developpers to contribute. The second option would maximize the performances. Performances should be considered very seriously because this system would be called for all statuses received by a Fediverse server.

Both directions also call for further extensions such as decentralized Machine Learning or hate speech detection.
