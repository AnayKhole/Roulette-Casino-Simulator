# Roulette Casino Simulator

A roulette game built with Python and Pygame, featuring an animated European roulette wheel, betting mechanics, a virtual balance system, and a casino bank that offers loans based on recent gameplay performance.

The project combines graphical programming, event-driven interaction, game-state management, and rule-based financial logic in an interactive desktop application.

Features

Animated Roulette Wheel

* European roulette layout with 37 numbered pockets (0–36).
* Traditional red, black, and green pocket colours.
* Smooth wheel rotation and a separately animated roulette ball.
* Dynamic visual effects, including a pulsing winning number and animated centre.
* Randomised outcomes for each spin.

Betting System

* Virtual starting balance of **$10,000**.
* Adjustable bet amounts using on-screen controls or direct text input.
* Six betting options:

  * **Red / Black** — bet on the pocket colour.
  * **Even / Odd** — bet on the number's parity.
  * **Low / High** — bet on numbers 1–18 or 19–36.
* Payout calculations based on the selected bet and final result.
* Balance tracking and notifications for wins and losses.

Dynamic Casino Banking

A simulated lending system that evaluates recent gameplay performance before making loan offers.

* Tracks game outcomes and calculates the win rate over the most recent 10 games.
* Requires at least three completed games before a loan request can be assessed.
* Offers standard loans with a performance-based lending amount and 5% interest for players with a win rate of at least 60%.
* Provides a separate high-risk lending option for players with a win rate of 50% or below, with interest rates determined by performance.
* Allows players to accept or decline loan offers.
* Tracks outstanding debt and automatically uses available balance to repay it after each spin.

Interactive Gameplay

* Mouse-driven interface for placing bets, spinning the wheel, and managing loans.
* Keyboard input for custom bet amounts.
* Real-time balance, recent results, messages, and win-rate information.
* A hidden, one-use cheat mode activated by clicking the wheel's centre four times, allowing experimentation with predetermined winning outcomes.

## Technologies

* **Python** — core application logic and game mechanics.
* **Pygame** — graphical interface, rendering, animation, mouse and keyboard input.
* **Math** — geometric calculations for wheel segments, ball positioning, and animated visual effects.
* **Random** — generation of roulette outcomes and spin parameters.
* **Time** — animation timing and temporary on-screen messages.

## How to Play

1. Launch the application.
2. Set your desired bet using the `+` and `−` controls, or click the bet amount field to enter a custom value.
3. Select one of the six available betting options.
4. Click **SPIN** to start the roulette wheel.
5. Wait for the wheel to stop and view the result.
6. Your balance and game history update automatically.
7. If your balance falls below your selected bet amount, use the **BANK** button to request a loan, subject to the game's lending rules.

**Controls**

* Mouse: interact with betting buttons, the wheel, and the banking interface.
* Keyboard: enter a custom bet amount; press `Enter` to apply it, `Backspace` to edit it, or `Escape` to cancel input.


Banking Rules

The simulated bank uses recent outcomes to determine loan eligibility and terms.

| Recent win rate         | Loan outcome                                                                   |
| ----------------------- | ------------------------------------------------------------------------------ |
| 50% or below            | Full requested amount offered at a higher, performance-dependent interest rate |
| Above 50% but below 60% | Standard loan denied                                                           |
| 60% or above            | Partial loan offer, capped at 90% of the requested amount, at 5% interest      |

At least three games must be completed before a loan request can be evaluated. Win rate is calculated from the last 10 games, or all completed games if fewer than 10 are available.

Loan interest is added to the outstanding debt when a loan is accepted. Available balance is then used to repay outstanding debt automatically after subsequent spins.

## Project Structure

The application is currently implemented as a single Python script, with its functionality organised into three main classes:

* `RouletteWheel` — manages wheel rotation, ball animation, spin outcomes, and wheel rendering.
* `BankSystem` — handles loan eligibility, interest calculations, loan offers, and the banking interface.
* `Game` — manages the main game loop, betting, balance, payouts, input handling, and interaction between the wheel and banking systems.

## Future Improvements

Potential improvements include:

* Refactoring the application into separate modules for the game, wheel, banking, and interface.
* Adding straight-up number, column, and dozen bets to the standard betting interface.
* Improving roulette outcome validation and testing payout calculations across all bet types.
* Adding automated tests for betting rules, loan eligibility, interest, and debt repayment.
* Introducing persistent statistics, session summaries, and configurable game settings.
* Improving interface scaling, accessibility, and error handling.

## Disclaimer

This is a recreational simulation using virtual currency. It does not involve real-money betting, real financial lending, or actual financial services. The banking system is a game mechanic rather than a realistic credit assessment model.
