using System;
using System.Configuration;
using System.IO;
using System.Net;
using System.Reflection;
using System.Windows;

namespace VREDInterface
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private string _vredServerUrl = ConfigurationManager.AppSettings["VREDServerUrl"];
        private string _pythonScript = ConfigurationManager.AppSettings["PythonScript"];
        private string _baseLoad = "{0}/python?value=load(\"{1}\")";
        private string _baseEval = "{0}/pythoneval?value={1}";
        private double previousSliderValue;

        public MainWindow()
        {
            InitializeComponent();
            UrlTextBox.Text = _vredServerUrl;
            previousSliderValue = WheelbaseSlider.Value;
        }

        private void StartButton_Click(object sender, RoutedEventArgs e)
        {
            var path = Path.Combine(AssemblyDirectory, _pythonScript);
            var url = string.Format(_baseLoad, UrlTextBox.Text, path);
            if (string.IsNullOrWhiteSpace(url) &&  !IsValidUrl(url))
            {
                MessageBox.Show("Please enter valid url");
            }
            else
            {
                previousSliderValue = WheelbaseSlider.Value = 0;
                SendMessageToVRED(url);
            }
        }

        private void WheelbaseSlider_Changed(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            var delta = WheelbaseSlider.Value - previousSliderValue;
            previousSliderValue = WheelbaseSlider.Value;
            var command = @"updateWheelBase(" + delta + ")";
            var url = string.Format(_baseEval, UrlTextBox.Text, command);
            SendMessageToVRED(url);
        }
        private void SendMessageToVRED(string url)
        {
            try
            {
                var httpWebRequest = (HttpWebRequest)WebRequest.Create(url);
                httpWebRequest.KeepAlive = false;
                var httpWebResponse = (HttpWebResponse)httpWebRequest.GetResponse();
                httpWebResponse.Close();
            }
            catch
            {
            }
        }

        private bool IsValidUrl(string url)
        {
            Uri uriResult;
            bool result = Uri.TryCreate(url, UriKind.Absolute, out uriResult) && uriResult.Scheme == Uri.UriSchemeHttp;
            return result;
        }
        private static string AssemblyDirectory
        {
            get
            {
                var codeBase = Assembly.GetExecutingAssembly().CodeBase;
                var uri = new UriBuilder(codeBase);
                var path = Uri.UnescapeDataString(uri.Path);
                return Path.GetDirectoryName(path);
            }
        }
    }
}
