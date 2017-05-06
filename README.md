# Mallet Utilities
Utilities for parsing / examining output from [Mallet](http://mallet.cs.umass.edu/index.php)

*These utilities require mallet-2.0.7*
***

The main script, `bamMallet.py`, runs analysis on a .mallet file with configuration options in `bamMalletConfig.json`, outputs the results into a specified directory structure, and creates some .csv files for use with Gephi, R, or other SNA applications.
It does *not* import topics into the .mallet format, as you will almost certainly want to configure different stop words and other options.

Once you have produced a .mallet file, you can invoke this utility by calling `bamMallet.py malletFileLocation bamMalletConfigFileName directoryLocation`

## Script Parameters:
1. `malletFileLocation`: The path to your .mallet file.

2. `bamMalletConfigFileName`: the path to your .json configuration file

3. `directoryLocation`: Where you want the output directory structure placed relative to the invoked script

***
## json Config File:
The script reads a config file like the one outlined below:

```javascript
{
	"malletInstallDirectory": "/Applications/mallet-2.0.7",
	"topicCounts" :[
		40,
		60,
		80,
		100,
		120,
		160,
		200,
		240,
		280
	],
	"optimizationIntervals":[
		10,
		50,
		100,
		500,
		1000,
		2000
	],
	"commands":
	[
		{
			"command": "--output-state",
			"output": "state.gz"
		},
		{
			"command": "--output-topic-keys",
			"output": "keys.txt"
		},
		{
			"command": "--output-doc-topics",
			"output": "topicsCompostion.txt"
		},
		{
			"command": "--word-topic-counts-file",
			"output": "topicCounts.txt"
		}
	]
}
```
### json parameters:
1. `malletInstallDirectory`: Where you installed Mallet

2. `topicCounts`: A list of the number of topic counts you want to run on your corpus

3. `optimizationIntervals`: A list of the different optimization intervals you want to run for each of your topic counts

4. `commands`: A list of Mallet commands that you want to run on each combination of topic count and optimization variables. Each command is specified by the `command` value, the output file name is specified by the `output` value. For a list of commands, see [http://mallet.cs.umass.edu/topics.php](http://mallet.cs.umass.edu/topics.php)

***
## Output

1. The script outputs your results into a directory structure that looks like this: `directory/topicCount/optimizationValue`, where `directory` is the location you specified in the command line, `topicCount` is one of the number of topics choices taken from you config file, and `optimizationValue` is an optimization interval, also taken from your config file.

2. Depending on your choice of commands in the config file, you will have a number of files in each directory. Using the "default" config, you will see the following:

 * `keys_[Edges].csv`: A .csv with `source` and `target` columns created from the `--output-topic-keys` mallet option. The `source` column is the topic number, while the `target` column is an individual word.

 * `keys.txt`: Standard output from the `--output-topic-keys` mallet option.

 * `state.gz`: Standard output from the `--output-state` mallet option.

 * `topicCounts_All[Edges].csv`: A .csv with `source`,`target`, and `frequency` columns created from the `--word-topic-counts-file` mallet option. The `source` column is the topic number, while the `target` column is an individual word, and the `frequency` column is number of times the word is assigned to the topic in the corpus. This .csv file lists *all* words displayed as a result of the `--word-topic-counts-file` mallet option.

 * `topicCounts_Shared[Edges].csv`: Exactly the same as the `topicCounts_All[Edges].csv` file, except *only* words that appear in *more than one* topic are listed.

 * `topicCounts.txt`: Standard output from the `--word-topic-counts-file` mallet option.

 * `topicsCompostion.txt`: Standard output from the `--output-doc-topics` mallet option.
