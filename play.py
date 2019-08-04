from blackjack import Blackjack


def train_ai(game):
    while True:
        try:
            userInput = int(input("For how many iterations should we train the AI ?\n"))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            break
    game.train_ai(userInput)


def run():
    game = Blackjack()
    print('This is a simple reinforcement learning based blackjack game')
    train_ai(game)
    while True:
        try:
            userInput = int(input("Great ! Would you like to play yourself or let the AI do the work ? \n1. AI\n2. Self\n"))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            if userInput == 1 or userInput == 2:
                break
            else:
                print("Not a valid option ! Please enter 1 or 2")
                continue
    if userInput == 1:
        game.play_ai()
    else:
        game.play()

    while True:
        print("\n\nCurrent scores:")
        print("Player: {}".format(game.player_score))
        print("Dealer: {}\n\n".format(game.dealer_score))
        while True:
            try:
                userInput = int(input("What do we do now ? \n1. AI Play\n2. Self Play\n3. Improve Model\n4. Exit\n"))
            except ValueError:
                print("Not an integer! Try again.")
                continue
            else:
                if userInput >= 1 or userInput <= 4:
                    break
                else:
                    print("Not a valid option ! Please enter 1 or 2")
                    continue

        if userInput == 1:
            game.play_ai()
        elif userInput == 2:
            game.play()
        elif userInput == 3:
            train_ai(game)
        elif userInput == 4:
            break
    return 0


if __name__ == "__main__":
    run()