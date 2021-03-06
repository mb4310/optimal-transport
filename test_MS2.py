import matplotlib.pyplot as plt 
import numpy as np

mu1 = [0,0]
cov1 = [[3,0],[0,3]]

mu2 = [5,5]
cov2 = [[4,2],[2,4]]

mu3 = [-5,-5]
cov3 = [[3,0], [0,3]]

mu4 = [-4, 4]
cov4 = [[4,3], [3,4]]

np.random.seed(42)

x = np.random.multivariate_normal(mu1, cov1, 1000)
y = np.random.multivariate_normal(mu2,cov2, 1000)
z = np.random.multivariate_normal(mu3,cov3, 1000)
w = np.random.multivariate_normal(mu4,cov4,1000)

plt.figure(1)
plt.scatter(x[:,0], x[:,1], alpha=0.2, marker='.')
plt.scatter(y[:,0], y[:,1], alpha=0.2, marker='.')
plt.scatter(z[:,0], z[:,1], alpha=0.2, marker='.')
plt.scatter(w[:,0], w[:,1], alpha=0.2, marker='.')


h = 2.0 			#Select your bandwidth, this is done by hand!
X = np.concatenate((x,y,z,w), axis=0)			#your data is given
N_x = X.shape[0]


def K(x):      #Mean zero Gaussian kernel
	return np.exp(-1 * np.linalg.norm(x)**2/(2 * h**2))


def grid_generator(a,b):   
	grid_centers = []
	bandwidths = []
	for i in np.arange(1, a):
		x = i/a
		for j in np.arange(1,b):
			y = j/b
			grid_centers.append([x,y])

	return np.array(grid_centers)

grid  = grid_generator(5,5)
grid = 20 * grid - np.array([10,10])
plt.scatter(grid[:,0],grid[:,1], marker='x')

def kernel_mean(s): #X is the set of data, s is the sample mean. This implementation is atrocious(!)
	x = np.zeros(s.shape)
	y = 0
	L = X-s
	for i in np.arange(N_x):
		x+= K(L[i,:])*X[i,:]
	for i in np.arange(N_x):
		y+=K(L[i,:])
	return x/y

def mean_shift_cluster(G, epsilon):				#G is an array of your initial cluster centers, epsilon is stopping threshold
	done = False
	nit = 0
	N_G = G.shape[0]
	while done == False:
		nit +=1 
		new_centers = np.empty(G.shape)
		for i in np.arange(N_G):
			new_centers[i,:] = kernel_mean(G[i,:])
		changes = np.sum(np.linalg.norm((new_centers - G), ord=2, axis=1))
		G = np.copy(new_centers)
		done = (changes <= epsilon) or (nit >= 25)
		print("Mean-shift iteration " + str(nit) + " completed, " + "global change was: " + str(changes))
	return G

S = mean_shift_cluster(grid, 10**(-1))
print(S)
print(grid)

plt.scatter(S[:,0], S[:,1], color='k', s=10)
plt.show()


