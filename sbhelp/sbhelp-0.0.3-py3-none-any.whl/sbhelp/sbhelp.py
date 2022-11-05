from bokeh.plotting import figure, show
# Our main plotting package (must have explicit import of submodules)
import bokeh.io
import bokeh.plotting
import numpy as np
import tensorflow as tf

# Enable viewing Bokeh plots in the notebook
bokeh.io.output_notebook()

def plotLoss(modelHist):
    fig = figure(title="Loss Vs Epoch", x_axis_label="Epoch", y_axis_label="Loss")
    fig.line(np.array(range(1, len(modelHist.history['loss'])+1)), modelHist.history['loss'], legend_label='Training Loss', line_width=2, color='blue')
    fig.line(np.array(range(1, len(modelHist.history['loss'])+1)), modelHist.history['val_loss'], legend_label='Validation Loss', line_width=2, color='red')
    show(fig)

def plotAccuracy(modelHist):
    fig = figure(title="Accuracy Vs Epoch", x_axis_label="Epoch", y_axis_label="Accuracy")
    fig.line(np.array(range(1, len(modelHist.history['accuracy'])+1)), modelHist.history['accuracy'], legend_label='Training Accuracy', line_width=2, color='green')
    fig.line(np.array(range(1, len(modelHist.history['accuracy'])+1)), modelHist.history['val_accuracy'], legend_label='Validation Accuracy', line_width=2, color='purple')
    show(fig)

def plotAccuracyBA(modelHist, modelHist2):
    fig = figure(title="Accuracy Vs Epoch", x_axis_label="Epoch", y_axis_label="Accuracy")
    fig.line(np.array(range(modelHist.epoch[0], (modelHist.epoch[-1])+1)), modelHist.history['accuracy'], legend_label='Training Accuracy', line_width=2, color='green')
    fig.line(np.array(range(modelHist.epoch[0], (modelHist.epoch[-1])+1)), modelHist.history['val_accuracy'], legend_label='Validation Accuracy', line_width=2, color='purple')
    fig.line([len(modelHist.history['accuracy'])-1, len(modelHist.history['accuracy'])-1], [0, 1], legend_label='After Fine Tuning', line_width=2, color='black')
    fig.line(np.array(range(modelHist2.epoch[0], (modelHist2.epoch[-1])+1)), modelHist2.history['accuracy'], legend_label='Training Accuracy', line_width=2, color='green')
    fig.line(np.array(range(modelHist2.epoch[0], (modelHist2.epoch[-1])+1)), modelHist2.history['val_accuracy'], legend_label='Validation Accuracy', line_width=2, color='purple')
    show(fig)

def plotLossBA(modelHist, modelHist2):
    fig = figure(title="Loss Vs Epoch", x_axis_label="Epoch", y_axis_label="Loss")
    fig.line(np.array(range(modelHist.epoch[0], (modelHist.epoch[-1])+1)), modelHist.history['loss'], legend_label='Training Loss', line_width=2, color='blue')
    fig.line(np.array(range(modelHist.epoch[0], (modelHist.epoch[-1])+1)), modelHist.history['val_loss'], legend_label='Validation Loss', line_width=2, color='red')
    fig.line([len(modelHist.history['loss'])-1, len(modelHist.history['loss'])-1], [0, 1], legend_label='After Fine Tuning', line_width=2, color='black')
    fig.line(np.array(range(modelHist2.epoch[0], (modelHist2.epoch[-1])+1)), modelHist2.history['loss'], legend_label='Training Loss', line_width=2, color='blue')
    fig.line(np.array(range(modelHist2.epoch[0], (modelHist2.epoch[-1])+1)), modelHist2.history['val_loss'], legend_label='Validation Loss', line_width=2, color='red')
    show(fig)

def saveCheckpoint(pathName):
    checkpointPath = pathName
    checkpointCallback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpointPath,
                                                            save_weights_only=True,
                                                            save_best_only=False,
                                                            save_freq='epoch')
    return checkpointCallback