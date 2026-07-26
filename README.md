# 🥾 Smart Footwear for Early Detection of Foot/Leg Ulcers

An IoT and Machine Learning based smart footwear system for real-time
monitoring and early prediction of diabetic foot ulcer risk.

## Table of Contents

-   Introduction
-   Objectives
-   Features
-   System Architecture
-   Workflow
-   Machine Learning Pipeline
-   Hardware Components
-   Software Stack
-   Pin Configuration
-   Project Structure
-   Installation
-   API Flow
-   Future Scope
-   Contributors
-   License

## Introduction

This project integrates ESP32, four FSR sensors, a DS18B20 temperature
sensor, FastAPI, SQLite, Streamlit, and a Random Forest model to monitor
foot pressure and temperature, then estimate ulcer risk.

## Objectives

-   Monitor plantar pressure
-   Monitor temperature
-   Predict ulcer risk
-   Display real-time dashboard
-   Support early detection

## Features

-   ESP32 firmware
-   4 FSR sensors
-   DS18B20 sensor
-   Wi-Fi communication
-   FastAPI backend
-   Random Forest prediction
-   SQLite storage
-   Streamlit dashboard

## System Architecture

``` text
FSR + Temperature
        |
      ESP32
        |
   HTTP POST
        |
     FastAPI
        |
 Random Forest
        |
     SQLite
        |
    Streamlit
```

## Workflow

``` text
Read Sensors
   |
Average Values
   |
Send JSON
   |
Predict Risk
   |
Store Data
   |
Display Dashboard
```

## Machine Learning Pipeline

``` text
Dataset -> Cleaning -> Training -> Random Forest -> model.pkl -> Prediction
```

## Hardware Components

-   ESP32
-   4× FSR Sensors
-   DS18B20
-   4×10kΩ Resistors
-   4.7kΩ Pull-up Resistor

## Software Stack

-   Arduino IDE
-   Python
-   FastAPI
-   Streamlit
-   SQLite
-   scikit-learn
-   Pandas

## Pin Configuration

  ESP32    Component
  -------- -----------
  GPIO34   FSR1
  GPIO36   FSR2
  GPIO32   FSR3
  GPIO33   FSR4
  GPIO4    DS18B20

## Project Structure

``` text
Hardware/
firmware/
README.md
main.py
app.py
model.pkl
dataset.csv
requirements.txt
```

## Installation

1.  Clone repository.
2.  Install requirements.
3.  Upload firmware.
4.  Run FastAPI.
5.  Run Streamlit.

## API Flow

``` text
ESP32 -> FastAPI -> Random Forest -> Database -> Dashboard
```

## Future Scope

-   Mobile app
-   Cloud support
-   Alerts
-   Doctor portal
-   More sensors

## License

MIT
