from agent import MiniClawAgent

if __name__ == '__main__':
    agent = MiniClawAgent()
    goal = input("enter your goal: ")
    agent.run(goal)