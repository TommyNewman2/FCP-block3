import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
import argparse  #Imports all required packages


def diff_lotka(LV, t, alpha, beta, delta, gamma):
    dxdt = (alpha * LV[0]) - (beta * LV[0] * LV[1])
    dydt = (delta * LV[0] * LV[1]) - (gamma * LV[1]) #Calculates the population change for both predators and prey

    grad = [dxdt, dydt]
    return grad

def solve_lotka(LV, t_max, alpha, beta, delta, gamma):
    t = np.linspace(0, t_max) #sets the timeframe
    lotka = odeint(diff_lotka, LV, t, (alpha, beta, delta, gamma)) #runs the differential equation
    return lotka, t

def plot_lotka(data, t, alpha_values):
    fig, axes = plt.subplots(len(alpha_values)) #sets the amount of subplots needed
    plt.suptitle("Lotka-Volterra Predator-Prey Model")

    for i, alpha in enumerate(alpha_values):
        ax = axes[i]
        ax.plot(t, data[i][:, 0], label=f'Prey (alpha={alpha})') #plots both predator and prey cycles with their respective alpha values
        ax.plot(t, data[i][:, 1], label=f'Predator (alpha={alpha})')
        ax.legend()

    plt.show()

def save_lotka(data, t, alpha_values, filename):
    fig, axes = plt.subplots(len(alpha_values))
    plt.suptitle("Lotka-Volterra Predator-Prey Model")

    for i, alpha in enumerate(alpha_values):
        ax = axes[i]
        ax.plot(t, data[i][:, 0], label=f'Prey (alpha={alpha})')
        ax.plot(t, data[i][:, 1], label=f'Predator (alpha={alpha})')
        ax.legend()

    plt.savefig(filename) #same as above just does not show the figure rather saves it

def main():
    args = parse_arguments()

    initials = args.initial[:2] #only take the first 2 numbers
    x = initials[0]
    y = initials[1]

    beta = args.beta
    delta = args.delta
    gamma = args.gamma
    t_max = 100
    LV = [x, y] #sets all values to their values inputted in the terminal

    alphas = args.alpha[:5]  # Take the first 5 alpha values

    data_list = []
    for alpha in alphas:
        if args.initial and args.alpha and args.beta and args.delta and args.gamma: #only runs if all are true
            lotka, t = solve_lotka(LV, t_max, alpha, beta, delta, gamma)
            data_list.append(lotka) #adds all data to a list

    if args.saveplot:
        save_lotka(data_list, t, alphas, args.saveplot) #calls the save plot function
        print("Plot saved")
    else:
        plot_lotka(data_list, t, alphas)  #calls the display plot function

def parse_arguments():
    parser = argparse.ArgumentParser(description="Graph some predator prey cycles for certain values.")
    parser.add_argument('--initial', type=int, required=True, nargs='+', help='Input 2 values for the initial value of prey and predator')
    parser.add_argument('--alpha', type=float, required=True, nargs='+', help='Input up to 5 values of alpha')
    parser.add_argument('--beta', type=float, required=True) #sets all the required arguments to required and to take input
    parser.add_argument('--delta', type=float, required=True)
    parser.add_argument('--gamma', type=float, required=True)
    parser.add_argument('--saveplot', type=str, 'Save the file with the given name')
    return parser.parse_args()

if __name__ == "__main__":
    main()
