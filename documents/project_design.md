# Project Design and Framework

## Prioritizing Climate Resilience Investments in Mexico: An IPCC-Based Decision Framework for International Development Cooperation

## 1. Background

Climate change is one of the defining development challenges of the twenty-first century. Rising temperatures, changing precipitation patterns and the increasing frequency of extreme weather events are placing growing pressure on communities, ecosystems and economic activities worldwide. However, the impacts of climate change are not distributed equally. Regions differ considerably in their environmental conditions, socioeconomic characteristics and institutional capacity to prepare for, respond to and recover from climate-related events.

Mexico is particularly exposed to a wide range of climate hazards, including droughts, floods, hurricanes, heatwaves and water scarcity. At the same time, significant regional disparities exist across its 32 federal entities in terms of poverty, infrastructure, access to basic services and economic development. These differences influence the ability of states to adapt to climate change and strengthen their long-term resilience.

International organizations, national governments and development agencies increasingly recognize the importance of evidence-based planning to support climate adaptation and sustainable development. The Intergovernmental Panel on Climate Change (IPCC) provides an internationally recognized conceptual framework for understanding climate risk through the interaction of hazards, exposure and vulnerability. This project adopts and adapts that framework to the Mexican context in order to develop a transparent, data-driven approach for assessing climate resilience at the state level.

## 2. Business Problem

International development cooperation organizations regularly support projects that strengthen climate resilience, reduce vulnerability and promote sustainable development. However, financial resources, technical expertise and implementation capacity are inherently limited. As a result, organizations must make strategic decisions about where investments are likely to generate the greatest impact.

Prioritizing territories for climate resilience investments is a complex task because climate risk is multidimensional. Decision-makers must consider not only the likelihood of climate-related hazards, but also the characteristics of the exposed population, existing socioeconomic vulnerabilities and the capacity of institutions and communities to adapt to changing environmental conditions. These factors are often measured through different indicators, produced by different institutions and reported independently, making integrated decision-making challenging.

This project addresses this challenge by developing a data-driven decision-support framework for the 32 Mexican states. By integrating official environmental, socioeconomic and development indicators within an IPCC-based conceptual framework, the project seeks to identify states where climate resilience investments could potentially achieve the greatest impact.

The analysis will classify Mexico’s 32 federal entities into three investment-priority groups:

High priority: immediate or substantial resilience investment may be required.
Medium priority: existing resilience capacities should be strengthened.
Low priority: conditions should be maintained and monitored.

The resulting framework is intended to support strategic planning by illustrating how publicly available data and analytical techniques can be combined to improve the prioritization of climate resilience investments in international development cooperation.

## 3. Research Question

Which Mexican states should be prioritized for climate resilience investments based on an IPCC-informed assessment of climate hazards, exposure, socioeconomic vulnerability and adaptive capacity?

### 3.1 Supporting Research Questions

1. How do Mexican states differ in terms of climate hazards, exposure, socioeconomic vulnerability and adaptive capacity?

2. Which indicators contribute most to differences in climate resilience across Mexican states?

3. Can Mexican states be classified into meaningful investment-priority groups using data-driven clustering techniques?

4. How can the resulting prioritization framework support evidence-based decision-making for international development cooperation?

## 4. Objectives

### General Objective
To develop a data-driven decision-support framework, adapted from the IPCC AR6 conceptual framework, to identify states that need immediate climate resilience investment that prioritizes Mexican states for climate resilience investments using official environmental and socioeconomic indicators.

### Specific Objectives

1. Collect and integrate official state-level environmental, climate and socioeconomic datasets from national and international sources.
2. Adapt the IPCC AR6 climate risk framework into an operational framework for investment prioritization at the state level.
3. Develop an analytical framework that integrates climate hazards, exposure, sensitivity and adaptive capacity into a transparent prioritization model.
4. Identify groups of Mexican states with similar climate resilience characteristics using the Climate Resilience Investment Priority Index (CRIPI) and clustering techniques.
5. Design an interactive dashboard that communicates investment priorities and supporting indicators for decision-makers.
6. Provide evidence-based recommendations that illustrate how the proposed framework could support strategic planning in international development cooperation.

## 5. Conceptual Framework

This project adopts and adapts the climate risk concepts presented in the Intergovernmental Panel on Climate Change (IPCC) Sixth Assessment Report (AR6) to develop a decision-support framework for prioritizing climate resilience investments across the 32 Mexican states.

According to the IPCC AR6, climate risk results from the interaction between climate-related hazards, the exposure of people and assets, and the vulnerability of affected systems. Vulnerability is determined by factors that influence both the sensitivity of a system to climate impacts and its capacity to anticipate, cope with, adapt to and recover from those impacts.

While the IPCC framework was developed to assess climate risk, this project adapts its conceptual structure to support investment prioritization. Rather than estimating climate risk itself, the proposed framework identifies states where climate resilience investments may generate the greatest development impact by integrating indicators that represent four complementary dimensions:

- Hazard: The occurrence or intensity of climate-related events that may negatively affect people, infrastructure and ecosystems.

- Exposure: The presence of populations, economic activities, infrastructure and natural systems that could be affected by climate hazards.

- Sensitivity: The socioeconomic characteristics that increase the susceptibility of communities to climate impacts.

- Adaptive Capacity: The ability of institutions, infrastructure and communities to prepare for, respond to and recover from climate-related events.

These four dimensions provide the conceptual basis for selecting indicators, constructing the Climate Investment Priority Index and classifying Mexican states into investment-priority groups through data-driven clustering techniques.

### Table 1. Adaptation of the IPCC AR6 Conceptual Framework for Climate Investment Prioritization

| Dimension | Definition | Example Indicators |
|-----------|------------|-------------------|
| Hazard | Climate-related events that may negatively affect people, infrastructure and ecosystems. | Drought frequency, flood occurrence, water stress, extreme temperatures |
| Exposure | Population, infrastructure and economic assets that could be affected by climate hazards. | Population density, urban population, agricultural land |
| Sensitivity | Socioeconomic characteristics that increase susceptibility to climate impacts. | Poverty rate, rural population, agricultural employment |
| Adaptive Capacity | The ability of communities and institutions to anticipate, prepare for, respond to and recover from climate impacts. | Education, access to drinking water, healthcare, internet access |

## 6. Methodology

The project follows an end-to-end data analytics workflow designed to transform official environmental and socioeconomic data into a decision-support framework for climate resilience investment prioritization.

### Phase 1. Conceptual Framework Design

The analysis begins with a review of the IPCC Sixth Assessment Report (AR6) conceptual framework for climate risk. Based on this framework, four analytical dimensions—Hazard, Exposure, Sensitivity and Adaptive Capacity—are adapted to support investment prioritization at the state level in Mexico.

### Phase 2. Data Collection

Official state-level datasets will be collected from national and international organizations, including CONEVAL, INEGI, CONAGUA and the United Nations Sustainable Development Goals database. Indicators will be selected according to their relevance to the four dimensions of the conceptual framework.

### Phase 3. Data Preparation

Using Python and the pandas library, datasets will be cleaned, standardized and integrated into a single master dataset. This phase includes harmonizing state identifiers, handling missing values, selecting variables and preparing the data for subsequent analysis.

### Phase 4. Exploratory Data Analysis

Exploratory data analysis will be conducted to understand the distribution of indicators, identify regional patterns, detect potential outliers and examine relationships between variables.

### Phase 5. Development of the Decision Framework

A Climate Resilience Investment Priority Index (CRIPI) will be constructed by integrating standardized indicators representing Hazard, Exposure, Sensitivity and Adaptive Capacity. The index will provide a transparent basis for comparing climate resilience investment needs across Mexican states.

### Phase 6. Clustering Analysis

An unsupervised machine learning approach (K-Means clustering) will be applied to classify the 32 Mexican states into three investment-priority groups based on the CRIPI.

### Phase 7. Visualization and Decision Support

The final analytical dataset will be exported to Tableau to create an interactive dashboard presenting investment-priority groups, indicator comparisons and geographic visualizations. The results will be interpreted to develop evidence-based recommendations illustrating how the proposed framework could support strategic decision-making in international development cooperation.

## 7. Expected Outputs

The project will deliver a transparent and reproducible decision-support framework that integrates official environmental and socioeconomic indicators to support climate resilience investment prioritization across the 32 Mexican states.

The expected outputs include:

Analytical Outputs
- A consolidated state-level analytical dataset integrating official environmental, climate and socioeconomic indicators.
- A Climate Resilience Investment Priority Index (CRIPI) constructed using the adapted IPCC AR6 conceptual framework.
- A classification of the 32 Mexican states into three investment-priority groups using unsupervised machine learning techniques.
  
Visualization Outputs
- An interactive Tableau dashboard presenting:
- Climate resilience investment priority groups.
- Geographic distribution of investment priorities.
- Comparative indicator profiles across states.
- Interactive filters and key performance indicators.
  
Decision-Support Outputs
- An IPCC-informed Climate Investment Prioritization Framework adapted to the Mexican context.
- State-level investment profiles highlighting the main factors influencing prioritization.
- Evidence-based policy recommendations illustrating how the framework could support strategic planning in international development cooperation.

Technical Outputs
- A fully reproducible GitHub repository containing:
- Python notebooks and scripts.
- Project documentation.
- Data dictionary.
- Methodological framework.
- Tableau dashboard files.
- Final README.

## 8. Timeline
https://trello.com/invite/b/6a71b3fec3caec6c6da43c58/ATTI1f6d98831c858b3e295bfdd43e1b08058C797641/final-project-ironhack

## 9. Project Limitations and Future Improvements

### 9.1 Limitations

Several limitations should be considered when interpreting the results:

- Geographic aggregation: The analysis is conducted at the state level. Consequently, important differences between municipalities or local communities within the same state are not captured.
- Data availability: The framework relies exclusively on publicly available official datasets. Some relevant climate resilience indicators may not be available at the state level or may differ in reporting years across institutions.
- Indicator selection: The selected indicators represent measurable proxies for the conceptual dimensions of Hazard, Exposure, Sensitivity and Adaptive Capacity. Although grounded in the IPCC AR6 framework, they do not capture every aspect of climate risk.
- Weighting methodology: All four conceptual dimensions will receive equal weights in the construction of the Climate Resilience Investment Priority Index (CRIPI). This decision prioritizes methodological transparency and reproducibility over subjective expert weighting schemes.
- Decision-support purpose: The framework is intended to support strategic decision-making by providing an evidence-based analytical tool. The resulting investment priorities should be interpreted as complementary inputs to policy analysis and expert assessment rather than definitive funding recommendations.

### 9.2 Future Improvements

Future research could strengthen the framework by incorporating municipal-level data, dynamic climate projections, additional environmental indicators, stakeholder-defined weighting schemes, and validation through expert consultation with climate adaptation and development practitioners.


