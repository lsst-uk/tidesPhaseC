from nicegui import ui, events
import pandas as pd
from io import StringIO
import plotly.graph_objects as go
import pysnid
import os
import asyncio
from contextlib import contextmanager
import numpy as np

speed_of_light = 2.998e5  # km/s


state = {'filename': None}

base_dir = os.path.dirname(__file__)
print('Hello World')

snidInputDict = {
    "phase": None,
    "redshift": None,
    "delta_phase": 5,
    "delta_redshift": None,
    "redshift_bounds": [0, None],
    "lbda_range": [4000, 8000],
    "set_it": True,
    "verbose": False,
    "quiet": True,
    "get_results": True,
    "rm_zeros": True
}
commonGalaxyLines = {
    "H_gal": {
        'lines': [4341, 4861, 6563],
        'redshift': 0,
        'velocity': 0,
        'plot': True,
        'color': '#1473E6'
    },
    "NII_gal": {
        'lines': [6548, 6583],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#6E1EFF'
    },
    "[OII]_gal": {
        'lines': [3727],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#D0D949'
    },
    "[OIII]_gal": {
        'lines': [4959, 5007],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FFB400'
    },
    "NaI_gal": {
        'lines': [5890, 5896],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#1473E6'
    },
    "MgII_gal": {
        'lines': [2798],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#F04E98'
    },
    "SII_gal": {
        'lines': [6717, 6731],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF8C00'
    },
    "CaIIHK_gal": {
        'lines': [3969, 3934],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF5C39'
    },
    "ZnII_gal": {
        'lines': [2025],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#9D50FF'
    },
    "CrII_gal": {
        'lines': [2056, 2062, 2066],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#C99FFF'
    },
    "FeII_gal": {
        'lines': [2249, 2260, 2343, 2374, 2382, 2586, 2599],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF4B4B'
    },
    "MnII_gal": {
        'lines': [2576, 2594],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#2D9D78'
    },
    "MgI_gal": {
        'lines': [2852],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#D83790'
    }
}

commonSNLines = {
    "H": {
        'lines': [3970, 4102, 4341, 4861, 6563],
        'redshift': 0,
        'velocity': 0,
        'plot': True,
        'color': '#1473E6'
    },
    "HeI": {
        'lines': [3889, 4471, 5876, 6678, 7065],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#D83790'
    },
    "HeII": {
        'lines': [3203, 4686, 5411, 6560, 6683, 6891, 8237],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#F04E98'
    },
    "CII": {
        'lines': [3919, 3921, 4267, 5145, 5890, 6578, 7231, 7236],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FFB400'
    },
    "CIII": {
        'lines': [4647, 4650, 5696, 6742, 8500, 8665],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF8C00'
    },
    "CIV": {
        'lines': [4658, 5801, 5812, 7061, 7726],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF5C39'
    },
    "NII": {
        'lines': [3995, 4631, 5005, 5680, 5942, 6482, 6611],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#6E1EFF'
    },
    "NIII": {
        'lines': [4634, 4641, 4687, 5321, 5327, 6467],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#9D50FF'
    },
    "NIV": {
        'lines': [3479, 3483, 3485, 4058, 6381],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#C99FFF'
    },
    "NV": {
        'lines': [4604, 4620, 4945],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF4B4B'
    },
    "OI": {
        'lines': [6158, 7772, 7774, 7775, 8446],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#2D9D78'
    },
    "[OI]": {
        'lines': [5577, 6300, 6363],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#43B02A'
    },
    "OII": {
        'lines': [3390, 3377, 4416, 6641, 6721, 3738, 3960, 4115, 4358, 4651],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#A7C636'
    },
    "[OII]": {
        'lines': [3726, 3729],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#D0D949'
    },
    "[OIII]": {
        'lines': [4363, 4959, 5007],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FFB400'
    },
    "OV": {
        'lines': [3145, 4124, 4930, 5598, 6500],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF8C00'
    },
    "OVI": {
        'lines': [3811, 3834],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF5C39'
    },
    "NaI": {
        'lines': [5890, 5896, 8183, 8195],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#1473E6'
    },
    "MgI": {
        'lines': [3829, 3832, 3838, 4571, 4703, 5167, 5173, 5184, 5528, 8807],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#D83790'
    },
    "MgII": {
        'lines': [2796, 2798, 2803, 4481, 7877, 7896],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#F04E98'
    },
    "SiII": {
        'lines': [4128, 4131, 5958, 5979, 6347, 6371],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FFB400'
    },
    "SII": {
        'lines': [5433, 5454, 5606, 5640, 5647, 6715],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF8C00'
    },
    "CaII": {
        'lines': [
            3159, 3180, 3706, 3737, 3934, 3969,
            8202, 8249, 8498, 8542, 8662
        ],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#FF5C39'
    },
    "[CaII]": {
        'lines': [7292, 7324],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#6E1EFF'
    },
    "FeII": {
        'lines': [4303, 4352, 4515, 4549, 4924, 5018, 5169, 5198, 5235, 5363],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#9D50FF'
    },
    "FeIII": {
        'lines': [4397, 4421, 4432, 5129, 5158],
        'redshift': 0,
        'velocity': 0,
        'plot': False,
        'color': '#C99FFF'
    }
}

commonLines = {**commonSNLines, **commonGalaxyLines}

ui.colors(
    H='#1473E6', HeI='#D83790', HeII='#F04E98', CII='#FFB400', CIII='#FF8C00',
    CIV='#FF5C39', NII='#6E1EFF', NIII='#9D50FF', NIV='#C99FFF', NV='#FF4B4B',
    OI='#2D9D78', OII='#A7C636', OIII='#FFB400', OV='#FF8C00', OVI='#FF5C39',
    NaI='#1473E6', MgI='#D83790', MgII='#F04E98',
    SiII='#FFB400', SII='#FF8C00',
    CaII='#FF5C39', CaIIHK='#FF5C39'
)


def commonLinesToArgIndex(inLines):
    """
    Processes the commonSNLines dictionary to extract all 'lines' values into a
    single list and creates a dictionary mapping the original keys to the
    corresponding indexes in the list.

    Args:
        inLines (dict): The commonSNLines dictionary.

    Returns:
        tuple: A tuple containing:
            - A list of all line values.
            - A dictionary mapping the original keys to the corresponding
              indexes in the list.
    """
    all_lines = []  # List to store all line values
    index_mapping = {}  # Dictionary to store the mapping of keys to indexes

    for key, value in inLines.items():
        if 'lines' in value:
            start_index = len(all_lines)  # Start index for this key
            all_lines.extend(value['lines'])  # Add the lines to the list
            end_index = len(all_lines)  # End index for this key
            # Map key to indexes
            index_mapping[key] = list(
                range(start_index, end_index)
            )

    return all_lines, index_mapping


allSNLines, allSNLinesIndex = commonLinesToArgIndex(commonSNLines)
allGalaxyLines, allGalaxyLinesIndex = commonLinesToArgIndex(commonGalaxyLines)


def csv_handler(event: events.UploadEventArguments):
    """
    Handles the upload of a CSV file, processes its content, and updates the application state.

    Args:
        event (events.UploadEventArguments): The event object containing details about the uploaded file,
                                             including its name and content.

    Side Effects:
        - Updates the global `state` dictionary with the uploaded file's name and its content as a pandas DataFrame.
        - Saves the processed DataFrame to a temporary file named 'tmpFile.txt' with space-separated values.
        - Displays a notification to the user indicating the successful upload of the file.
        - Calls the `plotInputSpectrum` function to process or visualize the uploaded data.

    Notes:
        - The function assumes the uploaded file is in a space-separated format.
        - The `state['table']` is updated with the DataFrame representation of the uploaded file.
        - Some commented-out code suggests additional functionality (e.g., creating a UI table) that is currently disabled.
    """
    filename = event.name
    state['filename'] = filename
    with StringIO(event.content.read().decode()) as f:
        df = pd.read_csv(f, sep='\s+')
        df.to_csv('tmpFile.txt', sep=' ', index=False, header=False)
        # if 'table' not in state:
        #     #state['table'] = ui.table.from_pandas(df)
        #     #state['table'].visible = False
        state['table'] = df
        # Notify user of successful upload
        ui.notify(f'Uploaded file: {filename}')
        plotInputSpectrum()


def plotInputSpectrum():
    """
    Plots the input spectrum from a DataFrame stored in the application state.

    This function checks if a DataFrame is present in the global `state` object
    under the key 'table'. If the DataFrame exists, it creates a scatter plot
    using the first two columns of the DataFrame and adds it to the figure.
    The plot is labeled with the filename stored in the `state` under the key
    'filename'. If no DataFrame is found, a notification is displayed to the user.

    Note:
        - The function assumes the presence of a global `state` object containing
          the DataFrame and filename.
        - The `fig` object is expected to support the `add_trace` method for adding
          a scatter plot.
        - The `plot` object is expected to support the `update` method for refreshing
          the plot.
        - The `ui.notify` method is used to display notifications to the user.

    Raises:
        KeyError: If the 'table' or 'filename' key is missing in the `state` object.
    """
    if 'table' in state:  # Check if a DataFrame exists in the state
        df = state['table']
        fig.add_trace(go.Scatter(x=df[df.columns[0]], y=df[df.columns[1]], mode='lines', name=state['filename']))
        plot.update()
    else:
        ui.notify('No data exists to plot!', color='red')



async def runPysnid():
    """
    Executes the SNID (SuperNova IDentification) classification process on an 
    uploaded file.

    This function runs the SNID algorithm with the specified parameters and 
    handles the results. It provides notifications to the user about the 
    success or failure of the classification and updates the application state 
    and plots accordingly.

    Returns:
        bool: True if the SNID classification is successful, False otherwise.

    Raises:
        Exception: If an error occurs during the SNID classification process.

    Notes:
        - The function uses parameters from the `snidInputDict` dictionary to 
          configure the SNID run.
        - Results are stored in the application state under the key `snidres`.
        - Notifications are displayed to the user via the `ui.notify` method.
        - The plot is updated using the `update_plot_snid_model` function if 
          classification is successful.
        - If the classification fails, the plot is cleared using the 
          `plotSNID.clear` method.
    """
    try:
        snidres = pysnid.run_snid(
            os.path.join(base_dir, 'tmpFile.txt'),
            redshift=snidInputDict['redshift'],
            phase=snidInputDict['phase'],
            delta_phase=snidInputDict['delta_phase'],
            delta_redshift=snidInputDict['delta_redshift'],
            redshift_bounds=snidInputDict['redshift_bounds'],
            lbda_range=snidInputDict['lbda_range']
        )
        if snidres is None:
            ui.notify("SNID fit failed. Nothing returned", color='red')
            plotSNID.clear()
            #asyncio.sleep(0.1)
            return False
        elif len(snidres.get_typing_result()) == 0:
            ui.notify("SNID fit failed. No typing result", color='red')
            plotSNID.clear()
            #asyncio.sleep(0.1)
            return False
        else:
            state['snidres'] = snidres
            ui.notify('SNID Done!')
            update_plot_snid_model()
            #asyncio.sleep(0.1)
            return True
    except Exception as e:
        ui.notify(f'SNID classification failed: {e}', color='red')
        #asyncio.sleep(0.1)
        return False
    
# State to track the current model index
current_model_index = {'index': 1, 'nmodels': 0}  


def update_plot_snid_model():
    """
    Update the SNID model plot with the selected model and its details.
    This function checks if SNID results are available in the application state.
    If available, it updates the plot with the input data and the selected model
    based on the current model index. It also adds annotations with details about
    the selected model, such as its type, redshift, phase, and rlap value.
    The function performs the following steps:
    - Clears existing traces and annotations from the plot.
    - Adds a trace for the input data.
    - Adds a trace for the selected model based on the current index.
    - Adds an annotation with details about the selected model.
    - Updates the plot.
    If the index is out of range or no SNID results are available, it notifies
    the user with an appropriate message.
    Raises:
        None
    Notes:
        - The function assumes that `state`, `current_model_index`, `figSNID`,
          and `plotSNID` are globally accessible.
        - The `snidres` object is expected to have attributes `nmodels`, `data`,
          and `models`, and a method `get_typing_result()` that returns a DataFrame.
    """
    if 'snidres' in state:  # Check if SNID results exist
        snidres = state['snidres']
        current_model_index['nmodels'] = snidres.nmodels
        bestMatches = snidres.get_typing_result().reset_index()
        bestMatches['no.'] = np.int32(bestMatches['no.'])
        index = current_model_index['index']

        snMatch = bestMatches['sn'].values[bestMatches['no.']==index][0]
        typeMain = bestMatches['typing'].values[bestMatches['no.']==index][0]
        typeSub = bestMatches['subtyping'].values[bestMatches['no.']==index][0]
        totalType = bestMatches['type'].values[bestMatches['no.']==index][0]
        redshift = bestMatches['z'].values[bestMatches['no.']==index][0]
        phase = bestMatches['age'].values[bestMatches['no.']==index][0]
        rlap = bestMatches['rlap'].values[bestMatches['no.']==index][0]
        modelDescription = f"{snMatch}: {totalType}<br> z = {redshift} | {phase}<br> rlap {rlap}"

        if 1 <= index <= snidres.nmodels:
            # Clear the existing traces
            figSNID.data = []
            # Add the input data trace
            figSNID.add_trace(go.Scatter(
                x=snidres.data['wavelength'], 
                y=snidres.data['flux'], 
                mode='lines', 
                name=f"{state['filename']}",
                line=dict(color='#b3b3b3', width=2, dash='solid'),  # Increased line width
                opacity=0.9  # Set semi-transparency
            ))
            # Add the model trace for the current index
            figSNID.add_trace(go.Scatter(
                x=snidres.models['wavelength'][index], 
                y=snidres.models['flux'][index], 
                mode='lines', 
                name=f"Rank {index}: {snMatch}",
                line=dict(color='#c9252d', width=3)  # Increased line width
            ))
            # Clear existing annotations
            
            figSNID.layout.annotations = []
            # Add the new annotation
            figSNID.add_annotation(
                x=snidres.models['wavelength'][index][0],
                y=np.max(snidres.models['flux'][index][100]) + 2*np.std(snidres.models['flux'][index][0:100]),
                text=modelDescription,
                showarrow=False,
                yshift=0,
                xanchor="center",  # Align the text to the center
                align="center",    # Align the text content to the center
                bgcolor="rgba(255, 255, 255, 1)",  # Set the background color to white with 90% transparency
                font=dict(color="#c9252d")  # Set the font color to red
            )
            plotSNID.update()
            #plotSNID.up
        else:
            ui.notify('Index out of range!', color='red')
    else:
        ui.notify('No SNID results to plot!', color='red')


def next_model():
    """
    Navigate to the next SNID model in the results.

    This function increments the current model index and updates the plot
    with the corresponding model. If the index exceeds the number of models,
    it loops back to the first model.

    Side Effects:
        - Updates the `current_model_index` dictionary.
        - Calls `update_plot_snid_model` to refresh the plot.
    """
    if 'snidres' in state:
        current_model_index['index'] += 1
        if current_model_index['index'] >= current_model_index['nmodels']:
            current_model_index['index'] = 1  # Loop back to the first model
        update_plot_snid_model()


def previous_model():
    """
    Navigate to the previous SNID model in the results.

    This function decrements the current model index and updates the plot
    with the corresponding model. If the index goes below 1, it loops to
    the last model.

    Side Effects:
        - Updates the `current_model_index` dictionary.
        - Calls `update_plot_snid_model` to refresh the plot.
    """
    if 'snidres' in state:
        current_model_index['index'] -= 1
        if current_model_index['index'] < 1:
            current_model_index['index'] = current_model_index['nmodels']  # Loop to the last model
        update_plot_snid_model()


def plotSNIDResults():
    """
    Plot the SNID results, including input data and the first model fit.

    This function checks if SNID results are available in the application state.
    If available, it adds traces for the input data and the first model fit
    to the SNID plot.

    Side Effects:
        - Updates the `figSNID` object with new traces.
        - Calls `plotSNID.update()` to refresh the plot.

    Raises:
        KeyError: If the 'snidres' key is missing in the `state` object.
    """
    if 'snidres' in state:  # Check if SNID results exist
        snidres = state['snidres']
        figSNID.add_trace(go.Scatter(
            x=snidres.data['wavelength'],
            y=snidres.data['flux'],
            mode='lines',
            name="Input data"
        ))
        figSNID.add_trace(go.Scatter(
            x=snidres.models['wavelength'][1],
            y=snidres.models['flux'][1],
            mode='lines',
            name="Model Fit"
        ))
        plotSNID.update()
    else:
        ui.notify('No data exists to plot!', color='red')


@contextmanager
def disable(button: ui.button):
    """
    Temporarily disables a UI button while executing a block of code.

    This function is a context manager that disables the given button
    when entering the context and re-enables it upon exiting, ensuring
    the button's state is restored even if an exception occurs.

    Args:
        button (ui.button): The UI button to be temporarily disabled.

    Yields:
        None: Allows the execution of the code block within the context.
    """
    button.disable()
    try:
        yield
    finally:
        button.enable()


async def run_snid_with_spinner(button: ui.button) -> None:
    """
    Executes the SNID classification process asynchronously while displaying a spinner 
    and disabling the provided button during execution.

    This function runs the `runPysnid` task asynchronously, notifies the user of the 
    success or failure of the SNID classification, and updates the plot with the SNID model.

    Args:
        button (ui.button): The button to be disabled while the SNID classification 
                            process is running.

    Returns:
        None
    """
    # with ui.row().classes('justify-center mt-4') as row:  # Create a row to position the spinner
    #     spinner = ui.spinner(size='xl')  # Display a spinner
    with disable(button):
        await asyncio.sleep(0.01) #I need this in the code to make async work to disable the button while snid is running, I don't know why
        # taskPySNID = runPysnid()  # Run the task asynchronously
        snidResponse = await runPysnid()  # Run the task asynchronously
        #print(snidResponse)
        if snidResponse:
            ui.notify('SNID classification completed!')
        else:
            ui.notify('SNID classification failed!', color='red')
        # spinner.visible = False
        # row.visible = False  # Hide the spinner row
        update_plot_snid_model()
    

def updateLinesVisibility(visibleYN, lineName):
    #print(f"Updating visibility of {lineName} to {visibleYN}")
    fig.for_each_shape(
    lambda trace: trace.update(visible=bool(visibleYN)) if trace.name == lineName else (),
)
    plot.update()


def velocityToDeltaRedshift(velocity):
    #print(f"Updating redshift from: {trace} to {redshift}")
    '''
    This function will convert the expansion velocity to a delta redshift
    that is subtracted off the current redshift to shift the line
    '''
    #print(f"Velcotity: {velocity}")
    deltaRedshift = (np.sqrt(1+(velocity/speed_of_light))/np.sqrt(1-(velocity/speed_of_light))) - 1
    return deltaRedshift

# # Temporarily commented out for testing
# def updateLinesRedshift(redshift):
#     #print(f"Updating redshift from: {trace} to {redshift}")
#     if len(str(redshift)) > 0:
#         redshift = float(redshift)
#         fig.for_each_shape(
#         lambda trace: trace.update(x0  = (float(trace.label['text']) * (1+float(redshift))), x1 = (float(trace.label['text']) * (1+float(redshift)))\
#                                     if trace.name in commonGalaxyLines.keys() or trace.name in commonSNLines.keys() else None)
#         )

def updateLinesVelocity(velocity, lineName):
    if len(velocity) > 0:
        velocity = float(velocity)
        #deltaRedshift = velocityToDeltaRedshift(velocity, lineName)
        #print(f"Updating redshift from: {trace} to {redshift}")
        commonLines[lineName]['velocity'] = velocity
        #print(f"Updating velocity of {lineName} to {velocity}")
        fig.for_each_shape(
        lambda trace: trace.update(x0 = (float(trace.label['text']) * (1+commonLines[trace.name]['redshift']-velocityToDeltaRedshift(velocity))) if trace.name == lineName else trace.x0, 
                                   x1 = (float(trace.label['text']) * (1+commonLines[trace.name]['redshift']-velocityToDeltaRedshift(velocity))) if trace.name == lineName else trace.x1)
        )
        plot.update()

def updateLinesRedshift(redshift):
    #print(f"Updating redshift from: {trace} to {redshift}")
    if len(str(redshift)) > 0:
        redshift = float(redshift)

        for i in commonLines:
            commonLines[i]['redshift'] = redshift
        
        fig.for_each_shape(
        lambda trace: trace.update(x0 = (float(trace.label['text']) * (1+commonLines[trace.name]['redshift']-velocityToDeltaRedshift(commonLines[trace.name]['velocity']))) if trace.name in commonLines else None, 
                                   x1 = (float(trace.label['text']) * (1+commonLines[trace.name]['redshift']-velocityToDeltaRedshift(commonLines[trace.name]['velocity']))) if trace.name in commonLines else None)
        )
        # fig.for_each_shape(
        # lambda trace: print(commonLines[trace.name]['redshift']\
        #                             if trace.name in commonLines else print('Whoops'))
        # )
        plot.update()

# def updateVelocity(velocity, lineName):
#     #print(f"Updating redshift from: {trace} to {redshift}")
#     '''
#     This function will convert the expansion velocity to a delta redshift
#     that is subtracted off the current redshift to shift the line
#     '''
#     deltaRedshift = -1 * (np.sqrt(1+(velocity/speed_of_light))/np.sqrt(1-(velocity/speed_of_light))) - 1

    
#     fig.for_each_shape(
#     lambda trace: trace.update(x0  = (float(trace.label['text']) + (1+float(redshift))), x1 = (float(trace.label['text']) * (1+float(redshift)))\
#                                 if trace.name in commonGalaxyLines.keys() or trace.name in commonSNLines.keys() else None))
#     )


    # plot.update()
# Function to clear all checkboxes
def clear_plot():
    fig.data = []
    plot.update()

fig = go.Figure()
fig.update_layout(
    xaxis_title="Observed Wavelength",
    yaxis_title="Flux",
    margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(
        x=1,  # Position the legend at the right edge of the plot
        y=1,  # Position the legend at the top edge of the plot
        xanchor="right",  # Anchor the legend to the right of its position
        yanchor="top",  # Anchor the legend to the top of its position
        bgcolor="rgba(255,255,255,0.5)",  # Semi-transparent background for better visibility
        bordercolor="black",
        borderwidth=1
    ),
    template="simple_white",
    xaxis=dict(range=[4000, 8000])  # Set the x-axis range
)

figSNID = go.Figure(layout={
            'xaxis': {
                'title': 'Observed Wavelength',
                'visible': True,
                'showticklabels': True, 
            },
            'yaxis': {
                'title': 'Flux',
                'visible': False,
                'showticklabels': False
            }
        })
figSNID.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    legend=dict(
        x=1,  # Position the legend at the right edge of the plot
        y=1,  # Position the legend at the top edge of the plot
        xanchor="right",  # Anchor the legend to the right of its position
        yanchor="top",  # Anchor the legend to the top of its position
        bgcolor="rgba(255,255,255,0.5)",  # Semi-transparent background for better visibility
        bordercolor="black",
        borderwidth=1
    ),
    template="simple_white"
)

for key, value in commonSNLines.items():
    if 'lines' in value:  # Ensure the dictionary contains 'lines'
        for line in value['lines']:
            fig.add_vline(
                x=line,  # The wavelength value
                line_width=3,  # Set the line width
                line_color=value['color'],  # Use the color from the dictionary
                line_dash="dash",  # Optional: Set the line style
                name=key,  # Use the key as the name
                visible=False,  # Initially set the line to be invisible
                label={'text': line, 'font': {'size': 11, 'color':'white',}, 'textposition': 'end'}  # Set font size to 5 and position to top left
            )
for key, value in commonGalaxyLines.items():
    if 'lines' in value:  # Ensure the dictionary contains 'lines'
        for line in value['lines']:
            fig.add_vline(
                x=line,  # The wavelength value
                line_width=4,  # Set the line width
                line_color=value['color'],  # Use the color from the dictionary
                line_dash="solid",  # Optional: Set the line style
                name=key,  # Use the key as the name
                visible=False, # Initially set the line to be invisible
                label={'text':line,} #I'm fudging here and using this unused variable to stroe the restframe wavelength  # Initially set the line to be invisible
                )


with ui.header():
    ui.label("TiDES Manual Classifier").classes('text-2xl font-bold p-4')

# @ui.page('/')
# def main():
ui.label('Upload a spectrum').classes('text-2xl font-bold p-4')
with ui.grid(columns=2).classes('w-full h-full'):
    with ui.row().classes('justify-center'):
        ui.upload(label="Upload Spectrum", on_upload=csv_handler, auto_upload=True)\
            .style('width: 50%; height: 50%; margin: 0 auto; text-align: center; font-size: 150%;')    
        
        ui.button('Clear plot', icon='layers_clear', on_click=lambda: (clear_plot()))\
            .style('width: 50%; margin: 10px auto; display: block;').classes('text-center')
    
    # fig.add_vline(x=3, line_width=1, line_color="red", line_dash="dash",name="H", visible=True)
    # fig.add_vline(x=4, line_width=1, line_color="blue", line_dash="solid",name="H", visible=True)

    #fig.update()
    #fig.update_shapes(dict(x0=[10,12], x1=[10,12], line_color="red", line_width=10, line_dash="dash", name='H'), visible=True)
    
    plot = ui.plotly(fig).style('aspect-ratio: 2 / 1;').classes('w-full justify-start')




# with ui.row().classes('justify-center'):
#     pass

with ui.expansion('Common Lines', icon='list').classes('w-full').props('dense'):
    ui.label('Redshift').classes('text-xl font-bold p-2')
    redshiftVariable = ui.input(label='Redshift', placeholder=None,
    on_change=lambda e: updateLinesRedshift(e.value),
    validation={
        'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
        'Input cannot be empty': lambda value: len(str(value)) > 0
    }).style('width: 90%;')

    ui.label('Supernova Lines').classes('text-xl font-bold p-2')
    with ui.grid(columns=7).classes('w-full'):
        with ui.row():
            ui.checkbox(text="H", on_change=lambda e: updateLinesVisibility(e.value, "H"))\
            .props(f'color=H')
            ui.input(label="H velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value,"H"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')
        with ui.row():
            ui.checkbox(text="HeI", on_change=lambda e: updateLinesVisibility(e.value, "HeI"))\
            .props(f'color=HeI')
            ui.input(label="HeI velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "HeI"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="HeII", on_change=lambda e: updateLinesVisibility(e.value, "HeII"))\
            .props(f'color=HeII')
            ui.input(label="HeII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "HeII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="CII", on_change=lambda e: updateLinesVisibility(e.value, "CII"))\
            .props(f'color=CII')
            ui.input(label="CII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "CII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="CIII", on_change=lambda e: updateLinesVisibility(e.value, "CIII"))\
            .props(f'color=CIII')
            ui.input(label="CIII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "CIII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="CIV", on_change=lambda e: updateLinesVisibility(e.value, "CIV"))\
            .props(f'color=CIV')
            ui.input(label="CIV velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "CIV"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="NII", on_change=lambda e: updateLinesVisibility(e.value, "NII"))\
            .props(f'color=NII')
            ui.input(label="NII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "NII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="NIII", on_change=lambda e: updateLinesVisibility(e.value, "NIII"))\
            .props(f'color=NIII')
            ui.input(label="NIII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "NIII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="NIV", on_change=lambda e: updateLinesVisibility(e.value, "NIV"))\
            .props(f'color=NIV')
            ui.input(label="NIV velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "NIV"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="NV", on_change=lambda e: updateLinesVisibility(e.value, "NV"))\
            .props(f'color=NV')
            ui.input(label="NV velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "NV"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="OI", on_change=lambda e: updateLinesVisibility(e.value, "OI"))\
            .props(f'color=OI')
            ui.input(label="OI velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "OI"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="[OI]", on_change=lambda e: updateLinesVisibility(e.value, "[OI]"))\
            .props(f'color=[OI]')
            ui.input(label="[OI] velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "[OI]"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="OII", on_change=lambda e: updateLinesVisibility(e.value, "OII"))\
            .props(f'color=OII')
            ui.input(label="OII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "OII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="[OII]", on_change=lambda e: updateLinesVisibility(e.value, "[OII]"))\
            .props(f'color=[OII]')
            ui.input(label="[OII] velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "[OII]"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="[OIII]", on_change=lambda e: updateLinesVisibility(e.value, "[OIII]"))\
            .props(f'color=[OIII]')
            ui.input(label="[OIII] velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "[OIII]"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="OV", on_change=lambda e: updateLinesVisibility(e.value, "OV"))\
            .props(f'color=OV')
            ui.input(label="OV velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "OV"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="OVI", on_change=lambda e: updateLinesVisibility(e.value, "OVI"))\
            .props(f'color=OVI')
            ui.input(label="OVI velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "OVI"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="NaI", on_change=lambda e: updateLinesVisibility(e.value, "NaI"))\
            .props(f'color=NaI')
            ui.input(label="NaI velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "NaI"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="MgI", on_change=lambda e: updateLinesVisibility(e.value, "MgI"))\
            .props(f'color=MgI')
            ui.input(label="MgI velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "MgI"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="MgII", on_change=lambda e: updateLinesVisibility(e.value, "MgII"))\
            .props(f'color=MgII')
            ui.input(label="MgII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "MgII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="SiII", on_change=lambda e: updateLinesVisibility(e.value, "SiII"))\
            .props(f'color=SiII')
            ui.input(label="SiII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "SiII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="SII", on_change=lambda e: updateLinesVisibility(e.value, "SII"))\
            .props(f'color=SII')
            ui.input(label="SII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "SII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="CaII", on_change=lambda e: updateLinesVisibility(e.value, "CaII"))\
                .props(f'color=CaII')
            ui.input(label="CaII velocity", placeholder="Enter velocity", value=None, 
                on_change=lambda e: updateLinesVelocity(e.value, "CaII"),
                validation={
                'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
                'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="[CaII]", on_change=lambda e: updateLinesVisibility(e.value, "[CaII]"))\
            .props(f'color=[CaII]')
            ui.input(label="[CaII] velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "[CaII]"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="FeII", on_change=lambda e: updateLinesVisibility(e.value, "FeII"))\
            .props(f'color=FeII')
            ui.input(label="FeII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "FeII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')

        with ui.row():
            ui.checkbox(text="FeIII", on_change=lambda e: updateLinesVisibility(e.value, "FeIII"))\
            .props(f'color=FeIII')
            ui.input(label="FeIII velocity", placeholder="Enter velocity", value=None, 
            on_change=lambda e: updateLinesVelocity(e.value, "FeIII"),
            validation={
            'Input must be a number': lambda value: value.replace('.', '', 1).isdigit(),
            'Input cannot be empty': lambda value: len(str(value)) > 0
            })\
            .style('width: 50%; margin-left: 10px;')
    with ui.row().classes('justify-center'):
        ui.separator()
    ui.label('Galaxy Lines').classes('text-xl font-bold p-2')
    with ui.grid(columns=8).classes('w-full'):
        ui.checkbox(text="H", on_change=lambda e: updateLinesVisibility(e.value, "H_gal"))\
            .props(f'color=H')
        ui.checkbox(text="NII", on_change=lambda e: updateLinesVisibility(e.value, "NII_gal"))\
            .props(f'color=NII')
        ui.checkbox(text="[OII]", on_change=lambda e: updateLinesVisibility(e.value, "[OII]_gal"))\
            .props(f'color=[OII]')
        ui.checkbox(text="[OIII]", on_change=lambda e: updateLinesVisibility(e.value, "[OIII]_gal"))\
            .props(f'color=[OIII]')
        ui.checkbox(text="NaI", on_change=lambda e: updateLinesVisibility(e.value, "NaI_gal"))\
            .props(f'color=NaI')
        ui.checkbox(text="MgII", on_change=lambda e: updateLinesVisibility(e.value, "MgII_gal"))\
            .props(f'color=MgII')
        ui.checkbox(text="SII", on_change=lambda e: updateLinesVisibility(e.value, "SII_gal"))\
            .props(f'color=SII')
        ui.checkbox(text="CaII HK", on_change=lambda e: updateLinesVisibility(e.value, "CaIIHK_gal"))\
            .props(f'color=CaIIHK')
        ui.checkbox(text="ZnII", on_change=lambda e: updateLinesVisibility(e.value, "ZnII_gal"))\
            .props(f'color=ZnII')
        ui.checkbox(text="CrII", on_change=lambda e: updateLinesVisibility(e.value, "CrII_gal"))\
            .props(f'color=CrII')
        ui.checkbox(text="FeII", on_change=lambda e: updateLinesVisibility(e.value, "FeII_gal"))\
            .props(f'color=FeII')
        ui.checkbox(text="MnII", on_change=lambda e: updateLinesVisibility(e.value, "MnII_gal"))\
            .props(f'color=MnII')
        ui.checkbox(text="MgI", on_change=lambda e: updateLinesVisibility(e.value, "MgI_gal"))\
            .props(f'color=MgI')

# with ui.row().classes('justify-center'):
#     # Add a button to clear all checkboxes
#     ui.button('Clear All Checkboxes', on_click=lambda: clear_checkboxes())\
#         .style('width: 50%; margin: 10px auto; display: block;').classes('text-center')



    

ui.separator()
ui.label('Classify the spectrum using SNID or SIREN').classes('text-2xl font-bold p-4')

    # "phase": None,
    # "redshift": None,
    # "delta_phase": 5,
    # "delta_redshift": None,
    # "redshift_bounds": [0, None],
    # "lbda_range": [4000, 8000],
    # "set_it": True,
    # "verbose": False,
    # "quiet": True,
    # "get_results": True,
    # "rm_zeros": True

with ui.grid(columns=2).classes('w-full h-full'):

    with ui.row().classes('justify-center'):
        with ui.expansion('SNID Input parameters', icon='terminal').classes('w-full'):
            with ui.grid(columns=2).classes('w-full'):
                ui.input(label='1. Redshift', placeholder=str(snidInputDict['redshift']),
                on_change=lambda e: snidInputDict.update({'redshift': e.value}),
                value=snidInputDict['redshift'],
                validation={'Input must be a number': lambda value: value.replace('.', '', 1).isdigit()})

                ui.input(label='2. Phase', placeholder=snidInputDict['phase'],
                on_change=lambda e: snidInputDict.update({'phase': e.value}),
                value=snidInputDict['phase'],
                validation={'Input must be a number': lambda value: value.replace('.', '', 1).replace('-', '', 1).isdigit()})

                ui.input(label='3. Delta Redshift', placeholder=None,
                on_change=lambda e: snidInputDict.update({'delta_redshift': e.value}),
                value=snidInputDict['delta_redshift'],
                validation={'Input must be a number': lambda value: (value.replace('.', '', 1).replace('-', '', 1).isdigit()) or (value == None)})

                ui.input(label='4. Delta Phase', placeholder=5,
                on_change=lambda e: snidInputDict.update({'delta_phase': e.value}),
                value=snidInputDict['delta_phase'],
                validation={'Input must be a number': lambda value: (value.replace('.', '', 1).replace('-', '', 1).isdigit()) or (value == None)})

                # ui.label('5. Wavelength Range')
                # min_max_range = ui.range(min=0, max=1, step=0.001, value={'min': 0, 'max': 1})\
                # .props('label-always')\
                # .style('margin-top: 20px;')\
                # .on_value_change(lambda e: (
                #     min_wavelength_input.set_value(e.value['min']),
                #     max_wavelength_input.set_value(e.value['max'])
                # ))
                min_redshift_input = ui.input(label='5. Min Redshift', value=snidInputDict['redshift_bounds'][0], 
                    on_change=lambda e: snidInputDict.update({'redshift_bounds': [float(e.value), snidInputDict['redshift_bounds'][1]]}) if e.value.replace('.', '', 1).isdigit() else None, 
                    validation={'Input must be a number': lambda value: value.replace('.', '', 1).isdigit()}).style('width: 90%;')

                max_redshift_input = ui.input(label='5. Max Redshift', value=snidInputDict['redshift_bounds'][1], 
                    on_change=lambda e: snidInputDict.update({'redshift_bounds': [snidInputDict['redshift_bounds'][0], float(e.value)]}) if e.value.replace('.', '', 1).isdigit() else None, 
                    validation={'Input must be a number': lambda value: value.replace('.', '', 1).isdigit()}).style('width: 90%;')

                min_max_range = {'min': 4000, 'max': 8000}  # Define min_max_range with default values

                min_wavelength_input = ui.input(
                    label='Min Wavelength',
                    value=min_max_range['min'],
                    on_change=lambda e: (
                        min_max_range.update({'min': float(e.value), 'max': min_max_range['max']}),
                        snidInputDict.update({'lbda_range': [float(e.value), snidInputDict['lbda_range'][1]]})
                    ) if e.value.replace('.', '', 1).isdigit() else None,
                    validation={
                        'Input must be a number': lambda value: value.replace('.', '', 1).isdigit()
                    }
                ).style('width: 90%;')

                max_wavelength_input = ui.input(
                    label='Max Wavelength',
                    value=min_max_range['max'],
                    on_change=lambda e: (
                        min_max_range.update({'min': min_max_range['min'], 'max': float(e.value)}),
                        snidInputDict.update({'lbda_range': [snidInputDict['lbda_range'][0], float(e.value)]})
                    ) if e.value.replace('.', '', 1).isdigit() else None,
                    validation={
                        'Input must be a number': lambda value: value.replace('.', '', 1).isdigit()
                    }
                ).style('width: 90%;')

                # with ui.grid(columns=2).classes('w-full'):
                #     ui.input(label='Min Wavelength', value=min_max_range.value['min'], 
                #         on_change=lambda e: min_max_range.set_value({'min': float(e.value), 'max': min_max_range.value['max']}) if e.value.replace('.', '', 1).isdigit() else None, 
                #         validation={'Input must be a number': lambda value: value.replace('.', '', 1).isdigit()}).style('width: 90%;')

                #     ui.input(label='Max Wavelength', value=min_max_range.value['max'], 
                #         on_change=lambda e: min_max_range.set_value({'min': min_max_range.value['min'], 'max': float(e.value)}) if e.value.replace('.', '', 1).isdigit() else None, 
                #         validation={'Input must be a number': lambda value: value.replace('.', '', 1).isdigit()}).style('width: 90%;')
            # ui.label().bind_text_from(min_max_range, 'value',
            #               backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')

            # ui.label('2. Click "Classify with SNID" to classify the spectrum using SNID.')
            # ui.label('3. Use "Previous Model" and "Next Model" buttons to navigate through the models.')
            # ui.label('4. Optionally, click "Classify with SIREN" for alternative classification.')
    
    with ui.row().classes('justify-center'):
        pass

    
    snidButton = ui.button('Classify with SNID', on_click=lambda e: run_snid_with_spinner(e.sender))\
        .style('width: 50%; margin: 0 auto; display: block;').classes('text-center')
    
    
    
    ui.button('Classify with SIREN', on_click=lambda: ui.notify('Classifying...'))\
        .style('width: 50%; margin: 0 auto; display: block;').classes('text-center')

    with ui.row().classes('justify-center'):
        ui.button('Previous Model', on_click=previous_model)\
            .style('margin: 0 10px; display: inline-block;').classes('text-center')
        ui.button('Next Model', on_click=next_model)\
            .style('margin: 0 10px; display: inline-block;').classes('text-center')
    
    with ui.row().classes('justify-center'):
        pass

    with ui.row().classes('justify-center'):
        
        plotSNID = ui.plotly(figSNID)\
            .style('width: 100%; aspect-ratio: 2 / 1;')\
            .classes('w-full justify-center')
        
    with ui.row().classes('justify-center'):
        pass

    snidTiDES_DB = ui.button('Send classification to TiDES DB')\
        .style('width: 50%; margin: 0 auto; display: block;').classes('text-center disabled')




# @ui.page('/')
# def main():
ui.run(title='TiDES Classifier',favicon='./favicon.ico', uvicorn_reload_excludes='*.conda/*', reload=True)


#ui.run(reload=False, port=native.find_open_port())
