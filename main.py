import gym
env = gym.make('BipedalWalker-v2')
env.reset()
for _ in range(500):
	env.render()
	action = env.action_space.sample()
	print('Action: ', action)
	observation, reward, done, info = env.step(action) # take a random action
	print('Reward: ', reward)
env.close()
