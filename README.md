# Pincer-Search
Implementation of Pincer Search Algorithm used in Data Mining in python 3

## Introduction

Pincer search algorithm is used to find the Most Frequent Sets in a transaction for a given items.

Another algorithm that does the same is 'a priory' algorithm , which is a bottom up approach.

In 'a priory algorithm' we build  a candidate set cK that keeps updating in every database pass from a set of single elements to their combinations.

On the other hand, the pincer search goes bottom up and top down at the same time, it maintains a *most frequent candidate set* that initially stores all the items in a set and as the bottom up approach keeps growing, it prunes a lot of items that were initially found to be infrequent.

This repository contains an implementation of the pincer search algorithm.

**Note**: If you find any mistake, feel free to create a pull request.

