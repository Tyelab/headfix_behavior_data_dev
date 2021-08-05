def grep_teams(team_selection=[], lab_basepath="Y:/"):
    """
    Grabs team list from server based on user's input.

    User can define which teams they want to use for their analyses and
    the function will glob the paths for their selection.

    Parameters
    ----------
    arg1: list
        List of strings for teams of interest
        Default is empty list
    arg2: string
        Basepath for server location on machine
        Default is Y:/ for mapped Windows drive


    Returns
    -------
    1. list
        List of team path grabbed from server successfully
    2. list
        List of teams not found
    """

    # Take basepath and glob all available files and directories
    team_glob = Path(lab_basepath).glob("{}".format("*"))

    # Check if no team was specifically asked for, tell user we're gathering all teams
    if team_selection == []:

        print("Gathering all teams...")

        # List comprehension for returning all directories in Tye Lab server
        team_list = [team for team in team_glob if team.is_dir()]

    else:

        # List comprehension for returning only directories user wants in the Tye Lab server
        team_list = [team for team in team_glob if team.name in team_selection and team.is_dir()]

    # Create temporary list for checking if selected teams exist
    tmp = []

    # For the teams that were globbed successfully, append the team to the temp list
    for globbed_team in team_list:
        tmp.append(globbed_team.name)

    # Compare team selection with returned teams using sets, convert to list
    missing_teams = list(set(team_selection) - set(tmp))

    # If the missing_teams list is empty, the program found all requested teams
    if missing_teams == []:
        print("Found All Selected Teams")

    # Else, some teams weren't found. Tell the user which teams weren't found.
    else:
        print("Failed to find team(s):", missing_teams)

    # Show user which teams were returned
    print("Teams Returned:")
    for team in team_list:
        print("{} ".format(team.name))

    # Return the list of projects gathered
    return team_list, missing_teams

def choose_projects(team_list, project_selection={}):
    """
    Generates project paths list based on user's selection.

    User can define which project they want to use for their analyses and
    this function generates the paths for their selection.

    Parameters
    ----------
    arg1: list
        List of strings for teams of interest from grep_teams()
    arg2: dict
        Dictionary of values that will be used to create specific
        paths for selected teams and their projects

    Returns
    -------
    1. list
        List of team/project Paths to grep in next steps
    """

    # Make dictionary using the teams in team_list as keys
    project_dict = {team: [] for team in team_list}

    # For each time in the team_list, append the Path name's project's values
    for team in team_list:
        project_dict[team].append(project_selection[team.name])

    # Make empty project list
    project_dir_list = []

    for team in project_dict.keys():
        for project in range(len(project_dict[team][0])):
            project_dir_list.append(team / project_dict[team][0][project])

    print("Returned Directories: ")

    for directory in project_dir_list:
        print(directory)

    return project_dir_list

def choose_animals(project_list, animal_group="all"):
    """
    Generates animal paths list based on user's selection.

    User can define which cohort of animals they want to use
    for their analyses. This function generates the paths for
    their selection that meet specified conditions.

    Parameters
    ----------
    arg1: list
        List of strings for projects of interest from choose_projects()
    arg2: str
        String of value for which animal paths to gather.
        Default value is all.

    Returns
    -------
    1. list
        List of team/project/animal Paths to grep in next steps
    """

    # Create empty animal list for path generation
    animal_list = []

    # If the animal group is left as default/specified as all, grab all animals
    if animal_group == "all":
        print("Grabbing all animals...")

        # For each project directory in the project list
        for project_dir in project_list:

            # For each animal globbed in the project directory
            for animal in project_dir.glob("*"):

                # Append the animal's path to the animal_list
                print(project_dir.name, animal.name)
                animal_list.append(animal)

    # Else, only select animals from the specified group
    else:
        print("Grabbing only {} animals...".format(animal_group))

        # Format the animal group with the user's input
        animal_group = "[A-Z]{2}" + animal_group + "\d{3}"

        # For each project_directory in project_list
        for project_dir in project_list:

            # For each animal globbed in project directory
            for animal in project_dir.glob("*"):

                # Use regex to grab only the requested animal
                r = re.search(animal_group, string=animal.name)

                # If the search returns None, the animal didn't match the request
                # Skip over it with pass.
                if r is None:
                    pass

                # If something is returned, take the match object's value and append
                # the animal to the project directory.
                else:
                    print(project_dir.name, r.group(0))
                    animal_list.append(project_dir / r.group(0))

    # Finally, return the list of animals
    return animal_list


def choose_data(animal_list, data_group=[], verbose=True):
    """
    Generates animal's data paths list based on user's selection.

    User can define which dataset to use for the animals they
    want to use for their analyses. This function generates the
    paths for their selection that meet specified conditions.

    Parameters
    ----------
    arg1: list
        List of paths for animals of interest from choose_animals()
    arg2: list
        List of strings for which datasets to gather.
        Default value is all.
    arg3: bool
        Boolean argument for verbose output of paths found or
        not found by the function. Default is True.

    Returns
    -------
    1. list
        List of team/project/animal/dataset Paths to grep in
        next steps
    """

    # Create empty data list for path generation
    data_dir_list = []

    # If data_group is left as default or specified as empty,
    # grab all folders
    if data_group == []:
        print("Grabbing all data folders...")

        # For each animal in the animal list
        for animal in animal_list:

            # For the data_dir in the globbed animal_path
            for data_dir in animal.glob("*"):

                # Append the data_dir to the data_list
                print("Grabbing", animal.name, data_dir.name)
                data_list.append(data)

    #TODO: Make verbose into its own function
    elif len(data_group) > 0 and verbose is True:
        print("Grabbing...")
        for data_type in data_group:
            print(data_type, "data")

        print("\nFrom Projects(s)...")
        project_list = list(set([project.parent.name for project in animal_list]))
        for project in project_list:
            print(project)

        print("\nIn Team(s)...")
        team_list = list(set([team.parent.parent.name for team in animal_list]))
        for team in team_list:
            print(team)
        print("\nFor Animals...")
        for animal in animal_list:
            print(animal.name)

        print("\nChecking for directories...")
        for animal in animal_list:
            for data_type in data_group:
                if (animal / data_type).is_dir():
                    print("Found", animal.name, data_type)
                    data_dir_list.append(animal / data_type)
                else:
                    print("Not Found!", animal.name, data_type)
    else:

        #TODO: Write a function for checking
        print("Grabbing specified directories...", "\n", data_group)

        for animal in animal_list:
            for data_type in data_group:
                if (animal / data_type).is_dir():
                    data_dir_list.append(animal / data_type)
                else:
                    print(animal.name, data_type, "Not Found!")

    # Tell user which directories were returned
    print("\nReturning Directories:")
    for data_dir in data_dir_list:
        print(data_dir)

    return data_dir_list


def grep_twop_raw_behavior_data(data_directory, convert_missing_data=False, verbose=True):
    """
    Checks whether raw 2P behavior data has been converted to .csv for all available days.

    Parameters
    ----------
    arg1: Path
        Parent directory of raw behavior data file

    arg2: bool
        Whether to invoke raw data file conversion through Bruker's raw converter
        Default False; no containerized ripper is in place (7/29/21)...

    arg3: bool
        Whether to print checking process for the user.
        Default True

    Returns
    -------
    1. list
        Existing raw behavior data file paths
    """

    checked_behavior_file_list = []

    missing_behavior_dir_list = []

    raw_behavior_dir_search = data_directory.glob("*/*")

    raw_behavior_dir_dict = {result.parent : [file for file in result.glob("*.csv")] for result in raw_behavior_dir_search if result.is_dir()}

    if verbose is True:
        for key in raw_behavior_dir_dict:
            print("\nChecking if", key.parents[1].name, key.parents[0].name, key.name, "raw behavior is converted...")
            if len(raw_behavior_dir_dict[key]) == 0:
                print("\nWARNING!!!", key.parents[1].name, key.parents[0].name, key.name, "raw behavior not converted!")
                missing_behavior_dir_list.append(raw_behavior_dir_dict[key])
            else:
                print(key.parents[1].name, key.parents[0].name, key.name,  "raw behavior converted!")
                checked_behavior_file_list.append(raw_behavior_dir_dict[key][0])

        print("\nReturning checked files:")
        for file in checked_behavior_file_list:
            print(file)


    else:
        # TODO: This should be a warning/exception that is logged and/or saved somewhere maybe...
        for key in raw_behavior_dir_dict:
            if len(raw_behavior_dir_dict[key]) == 0:
                print("WARNING!!!", key.parents[1].name, key.parents[0].name, key.name, "raw data not converted!")
            else:
                checked_behavior_file_list.append(raw_behavior_dir_dict[key][0])

    return checked_behavior_file_list


def grep_twop_behavior_config(checked_behavior_file_list):
    """
    Generates animal's configuration paths list based on user's selection

    Parameters
    ----------
    arg1: list
        List of paths for animals of interest from choose_data()

    Returns
    -------
    1. list
        List of 2P behavior configuration Paths
    """

    twop_config_list = []

    for directory in checked_behavior_file_list:
        parent_dir = directory.parents[1]
        search = parent_dir.glob("*config.json")
        for result in search:
            twop_config_list.append(result)

    return twop_config_list


def clean_2p_behavior(twop_raw_behavior_file, raw_keys=["Lick", "Airpuff", "Liquid", "Speaker"], df_keys=["on", "off"]):
    """
    Takes in raw 2P behavior file produced by Bruker and generates timestamps.

    Parameters
    ----------
    arg1: Path
        Path to raw behavior data
    arg2: list
        List of raw data keys to clean
        Default is Lick, Airpuff, Liquid, and Speaker data
    arg3: list
        List of keys to create for dataframe
        Default is onset AND offset of each event

    Returns
    -------
    1. dict
        Dictionary containing timestamps for each event
    """

    # Create list of requested keys by concatenating each value in the raw and df keys arguments
    requested_keys = []

    for raw_key in raw_keys:
        for df_key in df_keys:
            requested_keys.append(raw_key + "_" + df_key)


    # Do the cleaning for the supplied raw data file
    # Tell the user which file is being processed
    print("Cleaning:", twop_raw_behavior_file.name)

    # Adapting code by Kyle Fischer, June 2021 thru line 44
    # Read the raw .csv from Bruker's Voltage Recording
    raw_behavior_df = pd.read_csv(twop_raw_behavior_file, index_col="Time(ms)").rename(columns=lambda col:col.strip())

    # Any value below 3V is certainly noise.  Set them to zero by filtering the raw dataframe
    raw_behavior_df = raw_behavior_df > 3

    # Convert all values to int for pandas.DataFrame.diff() to yield negative values for stop times
    # and then perform the .diff() function and finally use .fillna() to eliminate NaN values
    raw_behavior_df = raw_behavior_df.astype(int).diff().fillna(0)

    # Create empty dictionary for cleaned timestamps
    cleaned_behavior_dict = {}

    # Query the raw datafile for each condition.  1 represents "On" signal while -1 represents "Off"
    for key in requested_keys:
        if "on" in key:
            cleaned_behavior_dict[key] = raw_behavior_df.query(key.split("_")[0] + " == 1").index.tolist()
        else:
            cleaned_behavior_dict[key] = raw_behavior_df.query(key.split("_")[0] + " == -1").index.tolist()

    return cleaned_behavior_dict

def get_2p_trialtypes(twop_config_file):
    """
    Takes in twop configuration file and gives trial types

    Parameters
    ----------
    arg1: Path
        Path two behavior configuration file

    Returns
    -------
    1. list
        Gives list of trial types
    """

    # Open the json file using json package
    with open(twop_config_file, "r") as inFile:

        # Read the config file
        config = inFile.read()

        # Decode the file with json.loads()
        config_contents = json.loads(config)

        # Gather the trial types from the configuration
        config_trial_types = config_contents["trialArray"]

    return config_trial_types


def build_base_stimulus_df(config_trial_types):
    """
    Creates trial DataFrame from configuration trial types

    Parameters
    ----------
    arg1: list
        List of trial types obtained from get_2p_trialtypes()

    Returns
    -------
    1. Pandas DataFrame
        Returns base dataframe of trial types
    """

    base_behavior_df = pd.DataFrame()

    liquid_counter = 0
    airpuff_counter = 0

    for (index, trial) in enumerate(config_trial_types):
        if trial == 1:
            liquid_counter += 1
            trial_name = "Trial_" + str(index + 1)
            trial_type = "Sucrose_" + str(liquid_counter)
            series = pd.Series(trial_type, dtype=str, name=trial_name)
            base_behavior_df = base_behavior_df.append(series)
        else:
            airpuff_counter += 1
            trial_name = "Trial_" + str(index + 1)
            trial_type = "Airpuff_" + str(airpuff_counter)
            series = pd.Series(trial_type, dtype=str, name=trial_name)
            base_behavior_df = base_behavior_df.append(series)

    base_behavior_df.reset_index(inplace=True)
    base_behavior_df.columns = ["trial", "trial_type"]


    return base_behavior_df


def build_cleaned_stimulus_df(clean_behavior_dict):
    """
    Creates cleaned stimulus dataframe of timestamps from cleaned behavior dictionary

    Parameters
    ----------
    1. dict
        Cleaned behavior dictionary from clean_2p_behavior()

    Returns
    -------
    1. Pandas DataFrame
        Dataframe of cleaned behavior timestamps per trial
    """

    if len(cleaned_behavior_dict["Airpuff_on"]) == 0:
        cleaned_stimulus_df_keys = [key for key in cleaned_behavior_dict if "Lick" not in key and "Airpuff" not in key]
    else:
        cleaned_stimulus_df_keys = [key for key in cleaned_behavior_dict if "Lick" not in key]

    cleaned_stimulus_df = pd.DataFrame(columns=cleaned_stimulus_df_keys)

    for key in cleaned_stimulus_df_keys:
        cleaned_stimulus_df[key] = pd.Series(cleaned_behavior_dict[key]).divide(1000)

    return cleaned_stimulus_df


def build_behavior_stimulus_df(base_df, clean_df):
    """
    Joins cleaned_stimulus_df and base_behavior_df into one DataFrame

    Parameters
    ----------
    1. Pandas DataFrame
        Base behavior dataframe (trial types)
    2. Pandas DataFrame
        Cleaned stimulus dataframe (timestamps)

    Results
    -------
    1. Pandas DataFrame
        Dataframe from united base and stimulus inputs
    """

    merged_behavior_df = base_df.join(clean_df, how="outer")

    return merged_behavior_df


def write_merged_behavior_hdf(checked_behavior_file, merged_behavior_df, config_trialtypes, lick_timestamps):
    """
    Writes hdf5 file of cleaned data for a given session to disk

    Parameters
    ----------
    1. Path
        Path of checked behavior
    2. pandas.Dataframe
        Cleaned behavior dataframe of trials and stimuli
    3. list
        List of trial types from configuration file
    4. list
        List of lick timestamps from cleaned_behavior_dict

    Returns
    -------
    None
    """


    filename_pattern = re.compile("\d{8}_[A-Z]{3}\d{3}_plane\d{1}")

    re_filename_result = re.search(pattern=filename_pattern, string=checked_behavior_file.name)

    hdf_filename = checked_behavior_file.parents[1] / (re_filename_result.group(0) + "_merged.h5")

    merged_behavior_df.set_index("trial", inplace=True)

    trial_types = pd.Series(config_trialtypes)

    lick_timestamps = pd.Series(lick_timestamps)

    hdf_store = pd.HDFStore(hdf_filename)

    hdf_store.append(value=merged_behavior_df, key="stimulus_timestamps")

    hdf_store.append(value=trial_types, key="trial_types")

    hdf_store.append(value=lick_timestamps, key="lick_timestamps")

    tables.file._open_files.close_all()
