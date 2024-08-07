# Fediverse Spam Filtering

This repo presents a spam filtering for Fediverse social media platforms. For now, the current version is only a proof of concept. 

## Spam filtering model

For spam filtering, we use a Naive Bayes model. This simple approach is classic for email spam filtering and was recently imported to the Fediverse in Pixelfed.
We intend to generalize this approach and provide more features (e.g., decentralized learning). 

## Model training

Spam filters are continually trained. Indeed, the spam filter integrates new (training) data over time to improve its performances. However, a major challenge in Machine Learning is to obtain "annotated" data: for spam filters, a list of messages with their respective type (spam or ham).

Our system gathers training data in three ways:

1. The administrator can submit some annotated data (e.g., public dataset).
2. The system identifies outliers (i.e., messages containing many unknown words) and asks the administrator to manually label them => This approach enables enriching the training data in a targeted manner.
3. The system randomly picks some messages submitted to the spam filtering and asks the administrator to manually label them => This approach verifies that the filter remains in line with the administrator's expectations.

This assisted data annotation minimizes the administrator's workload, while enriching the filtering quality. 

## Data storage

Our spam filter only uses an embedded key-value store. We create three tables: one for the model parameters, one for the outliers, and one for the randomly picked messages.

We do not store training data to minimize storage overhead.

## Extensions

Based on this PoC, two directions are possible:

1. Refine this Python implementation to improve its performances and quality (see `TODO.md`)
2. Reimplement this design in Rust to maximize the performances

The first option would simplify the implementation work and could motivate more external developpers to contribute. The second option would maximize the performances. Performances should be considered very seriously because this system would be called for all messages received by a Fediverse server.

Both directions also call for further extensions such as decentralized Machine Learning or hate speech detection.
