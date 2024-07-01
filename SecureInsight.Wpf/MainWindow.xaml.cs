using Google.Protobuf.Collections;
using Grpc.Core;
using Grpc.Net.Client;
using OxyPlot;
using OxyPlot.Axes;
using OxyPlot.Series;
using PythonCNNMetricsAnalysis;
using PythonCorpus;
using PythonDemonstrate;
using PythonLSTMMetricsAnalysis;
using PythonMakeCNNModel;
using PythonMakeLSTMModel;
using PythonMakeMLPModel;
using PythonMakeWord2VecModel;
using PythonMLPMetricsAnalysis;
using SecureInsight.Repository;
using System.ComponentModel;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Controls;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using ICSharpCode.AvalonEdit.Highlighting;
using ICSharpCode.AvalonEdit.Highlighting.Xshd;

namespace SecureInsight.Wpf
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        #region Properties
        private Button browseButton;
        private ListBox directoriesListBox;
        private readonly APP.ILSTMMetricService _lSTMMetricService;
        private readonly APP.IMLPMetricService _mLPMetricService;
        private readonly APP.ICNNMetricService _cNNMetricService;
        private readonly APP.IFileMerger _fileMerger;
        private readonly APP.ITokenizer _tokenizer;

        private readonly string FirstGrpcAddress = "http://localhost:50051";
        private readonly string SecondGrpcAddress = "http://localhost:50052";

        private PlotModel _accuracyPlotModel;
        public PlotModel AccuracyPlotModel
        {
            get { return _accuracyPlotModel; }
            set
            {
                _accuracyPlotModel = value;
                OnPropertyChanged("AccuracyPlotModel");
            }
        }

        private PlotModel _precisionPlotModel;
        public PlotModel PrecisionPlotModel
        {
            get { return _precisionPlotModel; }
            set
            {
                _precisionPlotModel = value;
                OnPropertyChanged("PrecisionPlotModel");
            }
        }

        private PlotModel _recallPlotModel;
        public PlotModel RecallPlotModel
        {
            get { return _recallPlotModel; }
            set
            {
                _recallPlotModel = value;
                OnPropertyChanged("RecallPlotModel");
            }
        }

        private PlotModel _f1_ScorePlotModel;
        public PlotModel F1_ScorePlotModel
        {
            get { return _f1_ScorePlotModel; }
            set
            {
                _f1_ScorePlotModel = value;
                OnPropertyChanged("F1_ScorePlotModel");
            }
        }


        public event PropertyChangedEventHandler PropertyChanged;
        #endregion

        public MainWindow(
                APP.ILSTMMetricService lSTMmetricService,
                APP.IMLPMetricService mLPMetricService,
                APP.ICNNMetricService cNNMetricService,
                APP.IFileMerger fileMerger,
                APP.ITokenizer tokenizer
                )
        {
            InitializeComponent();
            _lSTMMetricService = lSTMmetricService;
            _mLPMetricService = mLPMetricService;
            _cNNMetricService = cNNMetricService;
            _tokenizer = tokenizer;
            _fileMerger = fileMerger;

            compareComboBox1.SelectedIndex = 0;
            compareComboBox2.SelectedIndex = 1;
            languageComboBox.SelectedIndex = 0;
        }


        #region Corpus
        private void AddCorpusBox_Click(object sender, RoutedEventArgs e)
        {
            // Create a new StackPanel to hold the new elements
            StackPanel newPanel = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(5) };

            // Create a ComboBox and populate it with languages
            ComboBox cmbLanguages = new ComboBox { Width = 120, Margin = new Thickness(5) };
            cmbLanguages.SelectedIndex = 0;
            cmbLanguages.IsDropDownOpen = true;

            string[] languages = {
                "c", "c++","csharp","java","python","delphi","pascal","php","rust","javascript","typescript"};
            foreach (var lang in languages)
            {
                cmbLanguages.Items.Add(lang);
            }

            // Create a TextBox for URL input
            TextBox urlTextBox = new TextBox();
            urlTextBox.Width = 400;
            urlTextBox.Margin = new Thickness(5);
            urlTextBox.FontSize = 14;
            urlTextBox.GotFocus += UrlTextBox_GotFocus;
            urlTextBox.LostFocus += UrlTextBox_LostFocus;

            // Create a TextBox for the directory path
            TextBox directoryTextBox = new TextBox { Width = 300, Margin = new Thickness(5), IsReadOnly = true, Visibility = Visibility.Collapsed };

            // Create a Browse Button
            Button browseButton = new Button { Content = "Select folder please", Width = 120, Margin = new Thickness(5) };

            // Attach event handler to the Browse button
            browseButton.Click += (s, args) =>
            {
                CorpusBrowseButton_Click(s, args, directoryTextBox);
            };

            // Create a Send Button
            Button sendButton = new Button { Content = "Start", Width = 75, Margin = new Thickness(5) };
            sendButton.Click += (s, args) => CorpusSendButton_Click(s, args, directoryTextBox, urlTextBox, cmbLanguages, newPanel);

            // Create a ProgressBar
            ProgressBar progressBar = new ProgressBar
            {
                Width = 200,
                Height = 10,
                Visibility = Visibility.Collapsed // Initially hide the progress bar
            };

            // Create a Remove Button
            Button removeButton = new Button { Content = "Remove", Width = 75, Margin = new Thickness(5) };
            removeButton.Click += (s, args) => CorpusStackPanel.Children.Remove(newPanel);

            // Add the elements to the StackPanel in the desired order
            newPanel.Children.Add(cmbLanguages);
            newPanel.Children.Add(urlTextBox);
            newPanel.Children.Add(directoryTextBox);
            newPanel.Children.Add(browseButton);
            newPanel.Children.Add(sendButton);
            newPanel.Children.Add(progressBar);
            newPanel.Children.Add(removeButton);

            // Add the StackPanel to the main StackPanel
            CorpusStackPanel.Children.Add(newPanel);
        }

        private void UrlTextBox_GotFocus(object sender, RoutedEventArgs e)
        {
            // Clear the placeholder text when the TextBox gets focus
            TextBox textBox = (TextBox)sender;
            if (textBox.Text == "Enter remote URL here: https://github.com/example.git")
            {
                textBox.Text = "";
            }
        }

        private void UrlTextBox_LostFocus(object sender, RoutedEventArgs e)
        {
            // Restore the placeholder text if the TextBox loses focus and is empty
            TextBox textBox = (TextBox)sender;
            if (string.IsNullOrWhiteSpace(textBox.Text))
            {
                textBox.Text = "Enter remote URL here: https://github.com/example.git";
            }
        }

        private void CorpusBrowseButton_Click(object sender, RoutedEventArgs e, TextBox directoryTextBox)
        {
            // Open FolderBrowserDialog to select a directory
            using (var dialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    // Get the selected directory path and set it to the directoryTextBox
                    string selectedPath = dialog.SelectedPath;
                    directoryTextBox.Text = selectedPath;
                }
            }
        }

        private async void CorpusSendButton_Click(object sender, RoutedEventArgs e, 
            TextBox directoryTextBox, TextBox urlTextBox, ComboBox cmbLanguages, StackPanel panel)
        {
            StringBuilder builder = new StringBuilder();
            var ttt = "https://github.com/LauraWartschinski/VulnerabilityDetection.git";
            // Get the directory path and URL from the respective TextBoxes
            string languages = cmbLanguages.Text;
            string path = directoryTextBox.Text;
            string remote_URL = urlTextBox.Text;

            if (!string.IsNullOrEmpty(languages) && !string.IsNullOrEmpty(path) && !string.IsNullOrEmpty(remote_URL))
            {
                try
                {
                    using var channel = GrpcChannel.ForAddress(FirstGrpcAddress, new GrpcChannelOptions
                    {
                        MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                        MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                    });

                    var client = new PythonCorpusService.PythonCorpusServiceClient(channel);
                    var call = client.Start(new PythonCorpus.StartRequest
                    {
                        Language = languages,
                        RemoteUrl = remote_URL,
                        //RemoteUrl = ttt,
                        Path = path,
                    });

                    // Find the progress bar from the StackPanel
                    var progressBar = panel.Children.OfType<ProgressBar>().FirstOrDefault();
                    progressBar.Visibility = Visibility.Visible;

                    await foreach (var response in call.ResponseStream.ReadAllAsync())
                    {
                        // Update the UI with the progress
                        progressBar.Value = response.Progress;
                        await Task.Delay(10);

                        if (!string.IsNullOrEmpty(response.Status))
                        {
                            //CorpusShowResults.AppendText(builder.AppendLine(response.Status).ToString());
                            textEditor.AppendText(builder.AppendLine(response.Status).ToString());
                        }
                        else if (response.Result)
                        {
                            textEditor.AppendText(builder.AppendLine(response.Result.ToString()).ToString());
                        }
                    }
                }
                catch (Exception ex)
                {
                    textEditor.AppendText(builder.AppendLine(ex.Message).ToString());
                }
                finally
                {
                    directoryTextBox.Text = string.Empty;
                    urlTextBox.Text = string.Empty;
                }
            }
            else
            {
                textEditor.AppendText("Please fill the form!");
                System.Windows.MessageBox.Show("Please fill the form!");
            }
        }
        #endregion

        #region Tokenize
        private void AddTokenizeBox_Click(object sender, RoutedEventArgs e)
        {
            // Create a new StackPanel to hold the new elements
            StackPanel newPanel = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(5) };

            // Create a ComboBox and populate it with languages
            ComboBox cmbLanguages = new ComboBox { Width = 120, Margin = new Thickness(5) };
            cmbLanguages.SelectedIndex = 0;
            cmbLanguages.IsDropDownOpen = true;

            string[] languages = {
                "c", "c++","csharp","java","python","delphi","pascal","php","rust","javascript","typescript"
            };
            foreach (var lang in languages)
            {
                cmbLanguages.Items.Add(lang);
            }

            // Create a ComboBox with ChunkSizes
            ComboBox cmbChunkSize = new ComboBox { Width = 120, Margin = new Thickness(5) };
            cmbChunkSize.SelectedIndex = 0;
            cmbChunkSize.IsDropDownOpen = true;

            Label label = new Label { Width = 50, Content = "MB" };

            for (int i = 10; i <= 100; i+=10)
            {
                cmbChunkSize.Items.Add(i);
            }

            // Create a Browse Button
            Button browseButton = new Button { Content = "Select files...", Width = 75, Margin = new Thickness(5) };

            // Create a TextBox for the directory path
            directoriesListBox = new ListBox { Width = 300 };

            // Attach event handler to the Browse button
            browseButton.Click += (s, args) => TokenizeBrowseButton_Click(s, args, directoriesListBox);

            // Create a Send Button
            Button sendButton = new Button { Content = "Start", Width = 75, Margin = new Thickness(5) };
            sendButton.Click += (s, args) => TokenizeSendButton_Click(s, args, directoriesListBox, cmbChunkSize, cmbLanguages, newPanel);

            // Create a ProgressBar
            ProgressBar progressBar = new ProgressBar
            {
                Width = 100,
                Height = 15,
                Visibility = Visibility.Collapsed // Initially hide the progress bar
            };

            // Create a Remove Button
            Button removeButton = new Button { Content = "Remove", Width = 75, Margin = new Thickness(5) };
            removeButton.Click += (s, args) => TokenizeStackPanel.Children.Remove(newPanel);

            // Add the elements to the StackPanel in the desired order
            newPanel.Children.Add(cmbLanguages);
            newPanel.Children.Add(cmbChunkSize);
            newPanel.Children.Add(label);
            newPanel.Children.Add(browseButton);
            newPanel.Children.Add(directoriesListBox);
            newPanel.Children.Add(sendButton);
            newPanel.Children.Add(progressBar);
            newPanel.Children.Add(removeButton);

            // Add the StackPanel to the Tokenize StackPanel
            TokenizeStackPanel.Children.Add(newPanel);
        }

        private void TokenizeBrowseButton_Click(object sender, RoutedEventArgs e, ListBox directoryTextBox)
        {
            List<string> directories = SelectFolders();
            if (directories != null)
            {
                directoriesListBox.Items.Clear();
                foreach (string directory in directories)
                {
                    directoriesListBox.Items.Add(directory);
                }
            }
        }

        private List<string> SelectFolders()
        {
            List<string> directories = new List<string>();

            using (var dialog = new System.Windows.Forms.OpenFileDialog())
            {
                dialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";

                if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    directories.Add(dialog.FileName);

                    while (true)
                    {
                        var result = System.Windows.Forms.MessageBox.Show("Do you want to select another folder?", "Select More", System.Windows.Forms.MessageBoxButtons.YesNo);
                        if (result == System.Windows.Forms.DialogResult.Yes)
                        {
                            if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                            {
                                directories.Add(dialog.FileName);
                            }
                        }
                        else
                        {
                            break;
                        }
                    }
                }
            }

            return directories;
        }

        private async void TokenizeSendButton_Click(object sender, RoutedEventArgs e, ListBox directoryTextBox,
            ComboBox cmbChunkSize, ComboBox cmbLanguages, StackPanel panel)
        {
            StringBuilder builder = new StringBuilder();
            RepeatedField<string> inputPaths = new RepeatedField<string>();
            foreach (string item in directoriesListBox.Items)
            {
                inputPaths.Add(item);
            }

            int.TryParse(cmbChunkSize.Text, out int result);


            if (directoriesListBox.Items[0] != null)
            {
                if (cmbLanguages.Text== "csharp")
                {
                    _tokenizer.Tokenize(inputPaths.ToArray(), result, _fileMerger);
                }
                else
                {
                    try
                    {
                        using var channel = GrpcChannel.ForAddress(FirstGrpcAddress, new GrpcChannelOptions
                        {
                            MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                            MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                        });

                        var client = new PythonTokenizer.PythonTokenizerService.PythonTokenizerServiceClient(channel);
                        var tokenizerMessage = new PythonTokenizer.StartRequest();
                        tokenizerMessage.Language = cmbLanguages.Text;
                        tokenizerMessage.InputPaths.AddRange(inputPaths);
                        tokenizerMessage.ChunkSize = result;

                        var call = client.Start(tokenizerMessage);

                        // Find the progress bar from the StackPanel
                        var progressBar = panel.Children.OfType<ProgressBar>().FirstOrDefault();
                        progressBar.Visibility = Visibility.Visible;

                        await foreach (var response in call.ResponseStream.ReadAllAsync())
                        {
                            // Update the UI with the progress
                            progressBar.Value = response.Progress;
                            await Task.Delay(10);

                            if (!string.IsNullOrEmpty(response.Status))
                            {
                                //CorpusShowResults.AppendText(builder.AppendLine(response.Status).ToString());
                                TokenizeTextEditor.AppendText(builder.AppendLine(response.Status).ToString());
                            }
                            else if (response.Result)
                            {
                                TokenizeTextEditor.AppendText(builder.AppendLine(response.Result.ToString()).ToString());
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        TokenizeTextEditor.AppendText(builder.AppendLine(ex.Message).ToString());
                    }
                    finally
                    {
                        //directoryTextBox.Text = string.Empty;
                        //urlTextBox.Text = string.Empty;
                    }
                }
               
            }
            else
            {
                TokenizeTextEditor.AppendText("Please fill the form!");
                System.Windows.MessageBox.Show("Please fill the form!");
            }
        }
        #endregion

        #region Word2VecModel
        private void Word2VecBrowseTokenizedDataButton_Click(object sender, RoutedEventArgs e)
        {
            System.Windows.Forms.OpenFileDialog openFileDialog = new System.Windows.Forms.OpenFileDialog();
            openFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";
            if (openFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                Word2VecTokenizedDataPathTextBox.Text = openFileDialog.FileName;
            }
        }

        private void Word2VecBrowseModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    Word2VecModelPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private List<int> ParseIntegerList(string input)
        {
            try
            {
                return input.Split(',')
                            .Select(s => int.Parse(s.Trim()))
                            .ToList();
            }
            catch
            {
                return null;
            }
        }

        private async void Word2VecSaveButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable the Save button to prevent multiple clicks
            Word2VecSaveButton.IsEnabled = false;

            // Get the values from the textboxes
            string tokenizedDataPath = Word2VecTokenizedDataPathTextBox.Text;
            string modelPath = Word2VecModelPathTextBox.Text;

            // Parse the lists of integers
            List<int> vectorSize = ParseIntegerList(Word2VecVectorSizeTextBox.Text);
            List<int> iterations = ParseIntegerList(Word2VecIterationsTextBox.Text);
            List<int> minCount = ParseIntegerList(Word2VecMinCountTextBox.Text);

            int workers;
            if (!int.TryParse(Word2VecWorkersTextBox.Text, out workers))
            {
                MessageBox.Show("Invalid input for Workers. Please enter a valid integer.");
                return;
            }

            if (vectorSize == null || iterations == null || minCount == null)
            {
                MessageBox.Show("Invalid input for Vector Size, Iterations, or Min Count. Please enter comma-separated integers.");
                return;
            }

            try
            {
                using var channel = GrpcChannel.ForAddress(SecondGrpcAddress, new GrpcChannelOptions
                {
                    MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                    MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                });

                var client = new PythonMakeWord2VecModelService.PythonMakeWord2VecModelServiceClient(channel);
                var message = new PythonMakeWord2VecModel.StartRequest();
                if (languageComboBox.Text == "C#")
                    message.TokenizeLanquage = 1;

                message.TokenizedDataPath = tokenizedDataPath;
                message.ModelPath = modelPath;

                message.Iterations.AddRange(iterations);
                message.VectorSize.AddRange(vectorSize);
                message.MinCount.AddRange(minCount);

                message.Workers = workers;

                var call = client.Start(message);
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    // Update the UI with the progress
                    if (response.Result)
                    {
                        Word2VecSaveButton.IsEnabled = true;
                        MessageBox.Show("finished");
                    }
                }

            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show(ex.Message);
            }
            finally
            {
                //directoryTextBox.Text = string.Empty;
                //urlTextBox.Text = string.Empty;
            }

        }
        #endregion

        #region LSTMModel
        private void LSTMBrowseSamplesPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    LSTMSamplesPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private void LSTMBrowseSaveModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    LSTMSaveModelPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private void LSTMBrowseWord2VecModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            System.Windows.Forms.OpenFileDialog openFileDialog = new System.Windows.Forms.OpenFileDialog();
            openFileDialog.Filter = "Model files (*.model)|*.model|All files (*.*)|*.*";
            if (openFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                LSTMModelPathTextBox.Text = openFileDialog.SafeFileName;
            }
        }

        private (int, int, int) GetNumbers(string lstmModelPath)
        {
            int vectorSize = 0, minCount = 0, iteration = 0; // Initialize x, y, and z to 0
                                                             // Use a regular expression to match numbers
            Regex regex = new Regex(@"\d+");
            MatchCollection matches = regex.Matches(lstmModelPath);

            if (matches.Count == 4)
            {
                vectorSize = int.Parse(matches[1].Value);
                minCount = int.Parse(matches[2].Value);
                iteration = int.Parse(matches[3].Value);

                Console.WriteLine($"x = {vectorSize}; y = {minCount}; z = {iteration};");
            }
            else
            {
                Console.WriteLine("The expected number of matches was not found.");
            }

            return (vectorSize, minCount, iteration);
        }

        private async void LSTMSaveButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable the Save button to prevent multiple clicks
            LSTMSaveButton.IsEnabled = false;

            var modes = LSTMModeListBox.SelectedItems.Cast<ListBoxItem>().Select(item => item.Content.ToString()).ToList();
            string samplesPath = LSTMSamplesPathTextBox.Text;
            string saveModelPath = LSTMSaveModelPathTextBox.Text;
            (int vectorSize, int minCount, int iteration) = GetNumbers(LSTMModelPathTextBox.Text);

            if (!double.TryParse(LSTMDropoutTextBox.Text, out double dropout))
            {
                MessageBox.Show("Invalid input for Dropout. Please enter a valid decimal number.");
                LSTMSaveButton.IsEnabled = true; // Re-enable the Save button if there's an error
                return;
            }

            if (!int.TryParse(LSTMNeuronsTextBox.Text, out int neurons) ||
                !int.TryParse(LSTMEpochsTextBox.Text, out int epochs) ||
                !int.TryParse(LSTMBatchSizeTextBox.Text, out int batchsize))
            {
                MessageBox.Show("Invalid input for Neurons, Epochs, or Batch Size. Please enter valid integers.");
                LSTMSaveButton.IsEnabled = true; // Re-enable the Save button if there's an error
                return;
            }

            // Save logic here
            try
            {
                using var channel = GrpcChannel.ForAddress(SecondGrpcAddress, new GrpcChannelOptions
                {
                    MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                    MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                });

                var client = new PythonMakeLSTMModelService.PythonMakeLSTMModelServiceClient(channel);
                var message = new PythonMakeLSTMModel.StartRequest();

                message.Modes.AddRange(modes);
                message.SamplesPath = samplesPath;
                message.SaveModelPath = saveModelPath;
                message.Dropout = dropout;
                message.Neurons = neurons;
                message.Epochs = epochs;
                message.BatchSize = batchsize;

                message.VectorSize = vectorSize;
                message.MinCount = minCount;
                message.Iteration = iteration;


                var call = client.Start(message);
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    // Update the UI with the progress
                    if (response.Result)
                    {
                        LSTMSaveButton.IsEnabled = true;
                        MessageBox.Show("finished");
                    }
                }

            }
            catch (Exception ex)
            {
                LSTMSaveButton.IsEnabled = true;
                System.Windows.MessageBox.Show(ex.Message);
            }
            finally
            {
                //directoryTextBox.Text = string.Empty;
                //urlTextBox.Text = string.Empty;
            }


        }
        #endregion

        #region MLPModel
        private void MLPBrowseSaveModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    MLPSaveModelPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private async void MLPSaveButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable the Save button to prevent multiple clicks
            MLPSaveButton.IsEnabled = false;

            var modes = MLPModeListBox.SelectedItems.Cast<ListBoxItem>().Select(item => item.Content.ToString()).ToList();
            string saveModelPath = MLPSaveModelPathTextBox.Text;

            if (!int.TryParse(MLPEpochsTextBox.Text, out int epochs) ||
                !int.TryParse(MLPBatchSizeTextBox.Text, out int batchsize))
            {
                MessageBox.Show("Invalid input for Neurons, Epochs, or Batch Size. Please enter valid integers.");
                MLPSaveButton.IsEnabled = true; // Re-enable the Save button if there's an error
                return;
            }

            // Save logic here
            try
            {
                using var channel = GrpcChannel.ForAddress(SecondGrpcAddress, new GrpcChannelOptions
                {
                    MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                    MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                });

                var client = new PythonMakeMLPModelService.PythonMakeMLPModelServiceClient(channel);
                var message = new PythonMakeMLPModel.StartRequest();

                message.Modes.AddRange(modes);
                message.SaveModelPath = saveModelPath;
                message.Epochs = epochs;
                message.BatchSize = batchsize;

                var call = client.Start(message);
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    // Update the UI with the progress
                    if (response.Result)
                    {
                        MLPSaveButton.IsEnabled = true;
                        MessageBox.Show("finished");
                    }
                }

            }
            catch (Exception ex)
            {
                MLPSaveButton.IsEnabled = true;
                System.Windows.MessageBox.Show(ex.Message);
            }
            finally
            {
                //directoryTextBox.Text = string.Empty;
                //urlTextBox.Text = string.Empty;
            }


        }
        #endregion

        #region CNNModel
        private void CNNBrowseSaveModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    CNNSaveModelPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private async void CNNSaveButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable the Save button to prevent multiple clicks
            CNNSaveButton.IsEnabled = false;

            var modes = CNNModeListBox.SelectedItems.Cast<ListBoxItem>().Select(item => item.Content.ToString()).ToList();
            string saveModelPath = CNNSaveModelPathTextBox.Text;

            if (!int.TryParse(CNNEpochsTextBox.Text, out int epochs) ||
                !int.TryParse(CNNBatchSizeTextBox.Text, out int batchsize))
            {
                MessageBox.Show("Invalid input for Neurons, Epochs, or Batch Size. Please enter valid integers.");
                CNNSaveButton.IsEnabled = true; // Re-enable the Save button if there's an error
                return;
            }

            // Save logic here
            try
            {
                using var channel = GrpcChannel.ForAddress(SecondGrpcAddress, new GrpcChannelOptions
                {
                    MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                    MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                });

                var client = new PythonMakeCNNModelService.PythonMakeCNNModelServiceClient(channel);
                var message = new PythonMakeCNNModel.StartRequest
                {
                    SaveModelPath = saveModelPath,
                    Epochs = epochs,
                    BatchSize = batchsize,
                    EnableLogging = true // Enable logging callback
                };
                message.Modes.AddRange(modes);

                var call = client.Start(message);
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    if (!string.IsNullOrEmpty(response.Progress))
                    {
                        // Update the UI with the progress
                        Console.WriteLine(response.Progress);
                        // You can also update your UI elements here
                    }

                    if (response.Result)
                    {
                        CNNSaveButton.IsEnabled = true;
                        MessageBox.Show("Finished");
                    }
                }
            }
            catch (Exception ex)
            {
                CNNSaveButton.IsEnabled = true;
                MessageBox.Show(ex.Message);
            }
            finally
            {
                // Perform any necessary cleanup
            }

        }
        #endregion

        #region Demonstrate
        private void DemonstrateBrowseSamplesPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    demonstrateSamplesPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private void DemonstrateBrowseSaveModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    demonstrateSaveModelPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private void DemonstrateBrowseWord2VecModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            System.Windows.Forms.OpenFileDialog openFileDialog = new System.Windows.Forms.OpenFileDialog();
            openFileDialog.Filter = "Model files (*.model)|*.model|All files (*.*)|*.*";
            if (openFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                demonstrateModelPathTextBox.Text = openFileDialog.SafeFileName;
            }
        }

        private void DemonstrateBrowseSaveBlocksVisualPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    demonstrateSaveBlocksVisualPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private async void DemonstrateSaveButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable the Save button to prevent multiple clicks
            demonstrateSaveButton.IsEnabled = false;

            var modes = demonstrateListBox.SelectedItems.Cast<ListBoxItem>().Select(item => item.Content.ToString()).ToList();
            string samplesPath = demonstrateSamplesPathTextBox.Text;
            string saveModelPath = demonstrateSaveModelPathTextBox.Text;
            string saveBlocksVisualPath = demonstrateSaveBlocksVisualPathTextBox.Text;
            (int vectorSize, int minCount, int iteration) = GetNumbers(demonstrateModelPathTextBox.Text);
            int.TryParse(numberOfExampleTextBox.Text, out int numberOfExample);

            //if (modes.Count() == 0 ||
            //    int.TryParse(numberOfExampleTextBox.Text, out int numberOfExample) ||
            //    string.IsNullOrEmpty(samplesPath) ||
            //    string.IsNullOrEmpty(saveModelPath) ||
            //    string.IsNullOrEmpty(saveBlocksVisualPath) ||
            //    vectorSize == 0 || minCount == 0 || iteration == 0
            //    )
            //{
            //    MessageBox.Show("Invalid input.");
            //    demonstrateSaveButton.IsEnabled = true; // Re-enable the Save button if there's an error
            //    return;
            //}


            // Save logic here
            try
            {
                using var channel = GrpcChannel.ForAddress(SecondGrpcAddress, new GrpcChannelOptions
                {
                    MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                    MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                });

                var client = new PythonDemonstrateService.PythonDemonstrateServiceClient(channel);
                var message = new PythonDemonstrate.StartRequest();

                message.Modes.AddRange(modes);
                message.SamplesPath = samplesPath;
                message.SaveModelPath = saveModelPath;
                message.VectorSize = vectorSize;
                message.MinCount = minCount;
                message.Iteration = iteration;


                message.SaveBlocksVisualPath = saveBlocksVisualPath;
                message.NumberOfExample = numberOfExample;

                var call = client.Start(message);
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    // Update the UI with the progress
                    if (response.Result)
                    {
                        demonstrateSaveButton.IsEnabled = true;
                        MessageBox.Show("finished");
                    }
                }

            }
            catch (Exception ex)
            {
                demonstrateSaveButton.IsEnabled = true;
                System.Windows.MessageBox.Show(ex.Message);
            }
            finally
            {
                //directoryTextBox.Text = string.Empty;
                //urlTextBox.Text = string.Empty;
            }

            demonstrateSaveButton.IsEnabled = true;
        }
        #endregion

        #region LSTM Metrics
        private void LSTMMetricsBrowseSaveModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    LSTMMetricsSaveModelPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private async void LSTMMetricsSaveButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable the Save button to prevent multiple clicks
            LSTMMetricsSaveButton.IsEnabled = false;

            var modes = LSTMMetricsListBox.SelectedItems.Cast<ListBoxItem>().Select(item => item.Content.ToString()).ToList();
            string saveModelPath = LSTMMetricsSaveModelPathTextBox.Text;

            if (modes.Count() == 0 || string.IsNullOrEmpty(saveModelPath))
            {
                MessageBox.Show("Invalid input.");
                LSTMSaveButton.IsEnabled = true; // Re-enable the Save button if there's an error
                return;
            }
            try
            {
                using var channel = GrpcChannel.ForAddress(SecondGrpcAddress, new GrpcChannelOptions
                {
                    MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                    MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                });

                var client = new PythonLSTMMetricsAnalysisService.PythonLSTMMetricsAnalysisServiceClient(channel);
                var message = new PythonLSTMMetricsAnalysis.StartRequest();

                message.Modes.AddRange(modes);
                message.SaveModelPath = saveModelPath;

                var call = client.Start(message);
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    LSTMMetricsSaveButton.IsEnabled = true;
                    foreach (PythonLSTMMetricsAnalysis.Metrics metrics in response.Result)
                    {
                        StringBuilder builder = new StringBuilder();
                        builder.AppendLine($"****** {metrics.Mode} ******");
                        builder.AppendLine($"Accuracy = {metrics.Accuracy:F2}");
                        builder.AppendLine($"Precision = {metrics.Precision:F2}");
                        builder.AppendLine($"Recall = {metrics.Recall:F2}");
                        builder.AppendLine($"F1 Score = {metrics.F1Score:F2}");

                        string result = builder.ToString();

                        LSTMMetricsShowResults.AppendText(result);
                    }
                }

            }
            catch (Exception ex)
            {
                LSTMMetricsSaveButton.IsEnabled = true;
                System.Windows.MessageBox.Show(ex.Message);
            }
            finally
            {
                //directoryTextBox.Text = string.Empty;
                //urlTextBox.Text = string.Empty;
            }

            LSTMMetricsSaveButton.IsEnabled = true;
        }
        #endregion

        #region MLP Metrics
        private void MLPMetricsBrowseSaveModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    MLPMetricsSaveModelPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private async void MLPMetricsSaveButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable the Save button to prevent multiple clicks
            MLPMetricsSaveButton.IsEnabled = false;

            var modes = MLPMetricsListBox.SelectedItems.Cast<ListBoxItem>().Select(item => item.Content.ToString()).ToList();
            string saveModelPath = MLPMetricsSaveModelPathTextBox.Text;

            if (modes.Count() == 0 || string.IsNullOrEmpty(saveModelPath))
            {
                MessageBox.Show("Invalid input.");
                MLPSaveButton.IsEnabled = true; // Re-enable the Save button if there's an error
                return;
            }
            try
            {
                using var channel = GrpcChannel.ForAddress(SecondGrpcAddress, new GrpcChannelOptions
                {
                    MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                    MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                });

                var client = new PythonMLPMetricsAnalysisService.PythonMLPMetricsAnalysisServiceClient(channel);
                var message = new PythonMLPMetricsAnalysis.StartRequest();

                message.Modes.AddRange(modes);
                message.SaveModelPath = saveModelPath;

                var call = client.Start(message);
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    MLPMetricsSaveButton.IsEnabled = true;
                    foreach (PythonMLPMetricsAnalysis.Metrics metrics in response.Result)
                    {
                        StringBuilder builder = new StringBuilder();
                        builder.AppendLine($"****** {metrics.Mode} ******");
                        builder.AppendLine($"Accuracy = {metrics.Accuracy:F2}");
                        builder.AppendLine($"Precision = {metrics.Precision:F2}");
                        builder.AppendLine($"Recall = {metrics.Recall:F2}");
                        builder.AppendLine($"F1 Score = {metrics.F1Score:F2}");

                        string result = builder.ToString();

                        MLPMetricsShowResults.AppendText(result);
                    }
                }

            }
            catch (Exception ex)
            {
                MLPMetricsSaveButton.IsEnabled = true;
                System.Windows.MessageBox.Show(ex.Message);
            }
            finally
            {
                //directoryTextBox.Text = string.Empty;
                //urlTextBox.Text = string.Empty;
            }

            MLPMetricsSaveButton.IsEnabled = true;
        }
        #endregion

        #region CNN Metrics
        private void CNNMetricsBrowseSaveModelPathButton_Click(object sender, RoutedEventArgs e)
        {
            using (System.Windows.Forms.FolderBrowserDialog folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    CNNMetricsSaveModelPathTextBox.Text = folderBrowserDialog.SelectedPath;
                }
            }
        }

        private async void CNNMetricsSaveButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable the Save button to prevent multiple clicks
            CNNMetricsSaveButton.IsEnabled = false;

            var modes = CNNMetricsListBox.SelectedItems.Cast<ListBoxItem>().Select(item => item.Content.ToString()).ToList();
            string saveModelPath = CNNMetricsSaveModelPathTextBox.Text;

            if (modes.Count() == 0 || string.IsNullOrEmpty(saveModelPath))
            {
                MessageBox.Show("Invalid input.");
                CNNSaveButton.IsEnabled = true; // Re-enable the Save button if there's an error
                return;
            }
            try
            {
                using var channel = GrpcChannel.ForAddress(SecondGrpcAddress, new GrpcChannelOptions
                {
                    MaxReceiveMessageSize = 100 * 1024 * 1024, // 100 MB
                    MaxSendMessageSize = 100 * 1024 * 1024 // 100 MB
                });

                var client = new PythonCNNMetricsAnalysisService.PythonCNNMetricsAnalysisServiceClient(channel);
                var message = new PythonCNNMetricsAnalysis.StartRequest();

                message.Modes.AddRange(modes);
                message.SaveModelPath = saveModelPath;

                var call = client.Start(message);
                await foreach (var response in call.ResponseStream.ReadAllAsync())
                {
                    CNNMetricsSaveButton.IsEnabled = true;
                    foreach (PythonCNNMetricsAnalysis.Metrics metrics in response.Result)
                    {
                        StringBuilder builder = new StringBuilder();
                        builder.AppendLine($"****** {metrics.Mode} ******");
                        builder.AppendLine($"Accuracy = {metrics.Accuracy:F2}");
                        builder.AppendLine($"Precision = {metrics.Precision:F2}");
                        builder.AppendLine($"Recall = {metrics.Recall:F2}");
                        builder.AppendLine($"F1 Score = {metrics.F1Score:F2}");

                        string result = builder.ToString();

                        CNNMetricsShowResults.AppendText(result);
                    }
                }

            }
            catch (Exception ex)
            {
                CNNMetricsSaveButton.IsEnabled = true;
                System.Windows.MessageBox.Show(ex.Message);
            }
            finally
            {
                //directoryTextBox.Text = string.Empty;
                //urlTextBox.Text = string.Empty;
            }

            CNNMetricsSaveButton.IsEnabled = true;
        }
        #endregion

        #region Analysis
        private void CompareButton_Click(object sender, RoutedEventArgs e)
        {
            IEnumerable<LSTMMetric> lSTMMetrics = _lSTMMetricService.GetLatestMetrics();
            IEnumerable<MLPMetric> mLPMetrics = _mLPMetricService.GetLatestMetrics();
            IEnumerable<CNNMetric> cNNMetrics = _cNNMetricService.GetLatestMetrics();

            int comboBox1 = compareComboBox1.SelectedIndex;
            int comboBox2 = compareComboBox2.SelectedIndex;

            if (comboBox1 == 0 && comboBox2 == 0)//LSTM vs LSTM
            {
                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var lSTMMetric in lSTMMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = lSTMMetric.Mode,
                        Value1 = lSTMMetric.Accuracy,
                        Value2 = lSTMMetric.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("LSTM", "LSTM", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var lSTMMetric in lSTMMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = lSTMMetric.Mode,
                        Value1 = lSTMMetric.Precision,
                        Value2 = lSTMMetric.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("LSTM", "LSTM", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var lSTMMetric in lSTMMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = lSTMMetric.Mode,
                        Value1 = lSTMMetric.Recall,
                        Value2 = lSTMMetric.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("LSTM", "LSTM", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var lSTMMetric in lSTMMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = lSTMMetric.Mode,
                        Value1 = lSTMMetric.F1_Score,
                        Value2 = lSTMMetric.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("LSTM", "LSTM", "F1_Score", f1ScoreData);


            }
            if (comboBox1 == 0 && comboBox2 == 1)//LSTM vs MLP
            {

                var lSTMMLPMetrics = lSTMMetrics.Join(mLPMetrics, lstm => lstm.Mode, mlp => mlp.Mode, (lstm, mlp) => new { LSTM = lstm, MLP = mlp }).ToList();

                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var item in lSTMMLPMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = item.LSTM.Mode,
                        Value1 = item.LSTM.Accuracy,
                        Value2 = item.MLP.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("LSTM", "MLP", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var item in lSTMMLPMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = item.LSTM.Mode,
                        Value1 = item.LSTM.Precision,
                        Value2 = item.MLP.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("LSTM", "MLP", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var item in lSTMMLPMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = item.LSTM.Mode,
                        Value1 = item.LSTM.Recall,
                        Value2 = item.MLP.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("LSTM", "MLP", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var item in lSTMMLPMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = item.LSTM.Mode,
                        Value1 = item.LSTM.F1_Score,
                        Value2 = item.MLP.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("LSTM", "MLP", "F1_Score", f1ScoreData);


            }
            if (comboBox1 == 0 && comboBox2 == 2)//LSTM vs CNN
            {
                var lSTMCNNMetrics = lSTMMetrics.Join(cNNMetrics, lstm => lstm.Mode, cnn => cnn.Mode, (lstm, cnn) => new { LSTM = lstm, CNN = cnn }).ToList();

                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var item in lSTMCNNMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = item.LSTM.Mode,
                        Value1 = item.LSTM.Accuracy,
                        Value2 = item.CNN.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("LSTM", "CNN", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var item in lSTMCNNMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = item.LSTM.Mode,
                        Value1 = item.LSTM.Precision,
                        Value2 = item.CNN.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("LSTM", "CNN", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var item in lSTMCNNMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = item.LSTM.Mode,
                        Value1 = item.LSTM.Recall,
                        Value2 = item.CNN.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("LSTM", "CNN", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var item in lSTMCNNMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = item.LSTM.Mode,
                        Value1 = item.LSTM.F1_Score,
                        Value2 = item.CNN.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("LSTM", "CNN", "F1_Score", f1ScoreData);


            }
            /////////////////////////
            if (comboBox1 == 1 && comboBox2 == 1)//MLP vs MLP
            {
                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var mLPMetric in mLPMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = mLPMetric.Mode,
                        Value1 = mLPMetric.Accuracy,
                        Value2 = mLPMetric.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("MLP", "MLP", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var mLPMetric in mLPMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = mLPMetric.Mode,
                        Value1 = mLPMetric.Precision,
                        Value2 = mLPMetric.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("MLP", "MLP", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var mLPMetric in mLPMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = mLPMetric.Mode,
                        Value1 = mLPMetric.Recall,
                        Value2 = mLPMetric.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("MLP", "MLP", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var mLPMetric in mLPMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = mLPMetric.Mode,
                        Value1 = mLPMetric.F1_Score,
                        Value2 = mLPMetric.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("MLP", "MLP", "F1_Score", f1ScoreData);


            }
            if (comboBox1 == 1 && comboBox2 == 0)//MLP vs LSTM
            {
                var mLPLSTMMetrics = mLPMetrics.Join(cNNMetrics, mlp => mlp.Mode, lstm => lstm.Mode, (mlp, lstm) => new { MLP = mlp, LSTM = lstm }).ToList();

                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var item in mLPLSTMMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = item.MLP.Mode,
                        Value1 = item.MLP.Accuracy,
                        Value2 = item.LSTM.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("MLP", "LSTM", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var item in mLPLSTMMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = item.MLP.Mode,
                        Value1 = item.MLP.Precision,
                        Value2 = item.LSTM.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("MLP", "LSTM", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var item in mLPLSTMMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = item.MLP.Mode,
                        Value1 = item.MLP.Recall,
                        Value2 = item.LSTM.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("MLP", "LSTM", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var item in mLPLSTMMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = item.MLP.Mode,
                        Value1 = item.MLP.F1_Score,
                        Value2 = item.LSTM.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("MLP", "LSTM", "F1_Score", f1ScoreData);


            }
            if (comboBox1 == 1 && comboBox2 == 2)//MLP vs CNN
            {
                var mLPCNNMetrics = mLPMetrics.Join(cNNMetrics, mlp => mlp.Mode, cnn => cnn.Mode, (mlp, cnn) => new { MLP = mlp, CNN = cnn }).ToList();

                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var item in mLPCNNMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = item.MLP.Mode,
                        Value1 = item.MLP.Accuracy,
                        Value2 = item.CNN.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("MLP", "CNN", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var item in mLPCNNMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = item.MLP.Mode,
                        Value1 = item.MLP.Precision,
                        Value2 = item.CNN.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("MLP", "CNN", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var item in mLPCNNMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = item.MLP.Mode,
                        Value1 = item.MLP.Recall,
                        Value2 = item.CNN.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("MLP", "CNN", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var item in mLPCNNMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = item.MLP.Mode,
                        Value1 = item.MLP.F1_Score,
                        Value2 = item.CNN.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("MLP", "CNN", "F1_Score", f1ScoreData);


            }
            /////////////////////////
            if (comboBox1 == 2 && comboBox2 == 2)//CNN vs CNN
            {
                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var cNNMetric in cNNMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = cNNMetric.Mode,
                        Value1 = cNNMetric.Accuracy,
                        Value2 = cNNMetric.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("CNN", "CNN", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var cNNMetric in cNNMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = cNNMetric.Mode,
                        Value1 = cNNMetric.Precision,
                        Value2 = cNNMetric.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("CNN", "CNN", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var cNNMetric in cNNMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = cNNMetric.Mode,
                        Value1 = cNNMetric.Recall,
                        Value2 = cNNMetric.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("CNN", "CNN", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var cNNMetric in cNNMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = cNNMetric.Mode,
                        Value1 = cNNMetric.F1_Score,
                        Value2 = cNNMetric.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("CNN", "CNN", "F1_Score", f1ScoreData);


            }
            if (comboBox1 == 2 && comboBox2 == 1)//CNN vs MLP
            {
                var cNNMLPMetrics = mLPMetrics.Join(cNNMetrics, mlp => mlp.Mode, cnn => cnn.Mode, (cnn, mlp) => new { CNN = cnn, MLP = mlp }).ToList();

                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var item in cNNMLPMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = item.CNN.Mode,
                        Value1 = item.CNN.Accuracy,
                        Value2 = item.MLP.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("CNN", "MLP", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var item in cNNMLPMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = item.CNN.Mode,
                        Value1 = item.CNN.Precision,
                        Value2 = item.MLP.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("CNN", "MLP", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var item in cNNMLPMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = item.CNN.Mode,
                        Value1 = item.CNN.Recall,
                        Value2 = item.MLP.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("CNN", "MLP", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var item in cNNMLPMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = item.CNN.Mode,
                        Value1 = item.CNN.F1_Score,
                        Value2 = item.MLP.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("CNN", "MLP", "F1_Score", f1ScoreData);


            }
            if (comboBox1 == 2 && comboBox2 == 0)//CNN vs LSTM
            {
                var cNNLSTMMetrics = mLPMetrics.Join(cNNMetrics, lstm => lstm.Mode, cnn => cnn.Mode, (cnn, lstm) => new { CNN = cnn, LSTM = lstm }).ToList();

                // Generate Accuracy Plot Model
                var accuracyData = new List<DataViewModel>();
                foreach (var item in cNNLSTMMetrics)
                {
                    accuracyData.Add(new DataViewModel
                    {
                        Mode = item.CNN.Mode,
                        Value1 = item.CNN.Accuracy,
                        Value2 = item.LSTM.Accuracy,
                    });
                }
                AccuracyPlotModel = CreateBarChart("CNN", "LSTM", "Accuracy", accuracyData);

                // Generate Precision Plot Model
                var precisionData = new List<DataViewModel>();
                foreach (var item in cNNLSTMMetrics)
                {
                    precisionData.Add(new DataViewModel
                    {
                        Mode = item.CNN.Mode,
                        Value1 = item.CNN.Precision,
                        Value2 = item.LSTM.Precision,
                    });
                }
                PrecisionPlotModel = CreateBarChart("CNN", "LSTM", "Precision", precisionData);

                // Generate Recall Plot Model
                var recallData = new List<DataViewModel>();
                foreach (var item in cNNLSTMMetrics)
                {
                    recallData.Add(new DataViewModel
                    {
                        Mode = item.CNN.Mode,
                        Value1 = item.CNN.Recall,
                        Value2 = item.LSTM.Recall,
                    });
                }
                RecallPlotModel = CreateBarChart("CNN", "LSTM", "Recall", recallData);

                // Generate F1_Score Plot Model
                var f1ScoreData = new List<DataViewModel>();
                foreach (var item in cNNLSTMMetrics)
                {
                    f1ScoreData.Add(new DataViewModel
                    {
                        Mode = item.CNN.Mode,
                        Value1 = item.CNN.F1_Score,
                        Value2 = item.LSTM.F1_Score,
                    });
                }
                F1_ScorePlotModel = CreateBarChart("CNN", "LSTM", "F1_Score", f1ScoreData);

            }

            DataContext = this;
        }

        private PlotModel CreateBarChart(string model1, string model2, string metric, IList<DataViewModel> data)
        {
            var plotModel = new PlotModel { Title = metric };
            var categoryAxis1 = new CategoryAxis
            {
                Position = AxisPosition.Bottom,
                Key = "CategoryAxis1",
                ItemsSource = new[] { model1, model2 }
            };

            var valueAxis1 = new LinearAxis
            {
                Position = AxisPosition.Left,
                Minimum = 0,
                Maximum = 1,
                Title = metric
            };

            plotModel.Axes.Add(categoryAxis1);
            plotModel.Axes.Add(valueAxis1);

            foreach (var item in data)
            {
                var getColor = GetColor(item.Mode);
                var series = new ColumnSeries
                {
                    Title = item.Mode,
                    StrokeColor = getColor.Item1,
                    StrokeThickness = 1,
                    FillColor = getColor.Item2,
                    ItemsSource = new[]
                    {
                        new ColumnItem { Value = item.Value1 },
                        new ColumnItem { Value = item.Value2}
                    }
                };
                plotModel.Series.Add(series);
            }

            return plotModel;
        }

        private (OxyColor, OxyColor) GetColor(string mode)
        {
            if (mode == "xss")
                return (OxyColors.Black, OxyColors.Red);
            else if (mode == "remote_code_execution")
                return (OxyColors.CornflowerBlue, OxyColors.Plum);
            else if (mode == "command_injection")
                return (OxyColors.Blue, OxyColors.Brown);
            else if (mode == "path_disclosure")
                return (OxyColors.BurlyWood, OxyColors.CadetBlue);
            else if (mode == "xsrf")
                return (OxyColors.Coral, OxyColors.Cornsilk);
            else if (mode == "sql")
                return (OxyColors.DarkCyan, OxyColors.Magenta);
            else if (mode == "open_redirect")
                return (OxyColors.Linen, OxyColors.Lime);
            else
                return (OxyColors.Gray, OxyColors.GreenYellow); // Using OxyColors.Gray as a default color
        }

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
#endregion

public class DataViewModel
{
    public string Mode { get; set; }
    public double Value1 { get; set; }
    public double Value2 { get; set; }
}