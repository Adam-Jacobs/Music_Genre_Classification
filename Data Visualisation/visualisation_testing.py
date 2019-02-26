import feature_visualisation as vis

# TODO make a way to load in the data and keep it here instead of loading it in every time before a plot

if __name__ == "__main__":
    perplex_upper = int(input('Upper limit to perplexity: '))
    step_num = int(input('Step amount: '))
    num_tracks = int(input('Number of tracks to create the plot from: '))

    num_plots = perplex_upper / step_num
    print('This will generate ' + str(num_plots) + ' plots')

    for perplexity in range(step_num, perplex_upper, step_num):
        vis.create_tsne_plot(perplexity, num_tracks, 'perplexity=' + str(perplexity))