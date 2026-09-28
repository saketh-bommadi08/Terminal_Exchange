# Terminal Exchange

A terminal-based electronic exchange implemented in Python.

## Overview

This project implements a simplified electronic exchange focused on the
core mechanics of order submission, order-book management, order matching,
trade execution, partial fills, and trade history.

The project was built from scratch to understand and implement the core
logic behind an electronic exchange.

## Features

- User accounts with cash and holdings
- Buy and sell order submission
- Limit orders
- Buy and sell order books
- Price-based order sorting
- Order matching
- Partial order fills
- Trade execution
- Trade history
- Trade-history search by:
  - Order ID
  - Price
  - Quantity
  - Time
- Input validation for numeric inputs
- Terminal-based interactive interface

## Core Components

### User Management

Each user has:

- A unique user ID
- Cash balance
- Holdings

The account balance and holdings are updated when buy and sell orders
are placed.

### Order Book

The exchange maintains separate buy and sell order lists.

Buy orders are sorted by price in descending order, while sell orders
are sorted by price in ascending order.

This allows the matching engine to access the best available bid and
ask at the front of the respective order lists.

### Matching Engine

The matching engine compares the best available buy and sell orders.

A trade can occur when:


Best Bid >= Best Ask
When orders match, the engine determines the execution price and
quantity.

It also handles partially filled orders when the quantities of the
matching orders are different.

### Trade History

Every executed trade is recorded with:

-  Trade ID
-  Execution price
-  Execution quantity
-  Execution time

The trade history can be viewed and searched using different criteria.

## Technologies
Python
tabulate
Python standard library

## How to run
Clone the repository and run:

python Exchange.py

## Project Structure
Terminal-Exchange   
│  
├── Exchange.py     
└── README.md

## Project Status
Working terminal-based exchange prototype implementing the core
exchange workflow from order submission through matching and trade
execution.