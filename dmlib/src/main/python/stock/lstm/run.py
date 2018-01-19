import lstm
import time
import matplotlib.pyplot as plt
import numpy as np


def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()


def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    # Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()


# Main Run Thread
if __name__ == '__main__':
    global_start_time = time.time()
    epochs = 1
    seq_len = 5

    print('> Loading data... ')

    X_train, y_train, X_test, y_test = lstm.load_data('000977.csv', seq_len, True)

    print('X_train shape:', X_train.shape)  # (3709L, 50L, 1L)
    print('y_train shape:', y_train.shape)  # (3709L,)
    print('X_test shape:', X_test.shape)  # (412L, 50L, 1L)
    print('y_test shape:', y_test.shape)  # (412L,)

    print('> Data Loaded. Compiling...')

    model = lstm.build_model([1, 5, 10, 1])

    model.fit(X_train, y_train, batch_size=512, nb_epoch=epochs, validation_split=0.05)

    # multiple_predictions = lstm.predict_sequences_multiple(model, X_test, seq_len, prediction_len=50)
    # print('multiple_predictions shape:', np.array(multiple_predictions).shape)  # (8L,50L)
    #
    # full_predictions = lstm.predict_sequence_full(model, X_test, seq_len)
    # print('full_predictions shape:', np.array(full_predictions).shape)  # (412L,)

    point_by_point_predictions = lstm.predict_point_by_point(model, X_test)
    print('point_by_point_predictions shape:', np.array(point_by_point_predictions).shape)  # (412L)

    print('Training duration (s) : ', time.time() - global_start_time)

    # plot_results_multiple(multiple_predictions, y_test, 50)
    # plot_results(full_predictions, y_test)
    plot_results(point_by_point_predictions, y_test)
