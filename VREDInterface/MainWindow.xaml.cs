using System;
using System.Configuration;
using System.IO;
using System.Net;
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

        public MainWindow()
        {
            InitializeComponent();
            UrlTextBox.Text = _vredServerUrl;
        }

        private void StartButton_Click(object sender, RoutedEventArgs e)
        {
            var url = string.Format(_baseLoad, UrlTextBox.Text, _pythonScript);
            if (string.IsNullOrWhiteSpace(url) &&  !IsValidUrl(url))
            {
                MessageBox.Show("Please enter valid url");
            }
            else
            {
                WheelbaseSlider.Value = 0;
                SendMessageToVRED(url);
            }
        }

        private void WheelbaseSlider_Changed(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            var command = @"updateWheelBase(" + WheelbaseSlider.Value + ")";
            var url = string.Format(_baseEval, UrlTextBox.Text, command);
            WheelbaseValue.Content = WheelbaseSlider.Value;
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
            catch (WebException exception)
            {
                var responseMessage = "";
                if (exception != null && exception.Response != null)
                {
                    responseMessage = new StreamReader(exception.Response.GetResponseStream()).ReadToEnd();
                }
                else
                {
                    responseMessage = exception.ToString();
                }
                //MessageBox.Show("Error while messaging VRED. Please check the settings. Details - " + responseMessage);
            }
        }

        private bool IsValidUrl(string url)
        {
            Uri uriResult;
            bool result = Uri.TryCreate(url, UriKind.Absolute, out uriResult) && uriResult.Scheme == Uri.UriSchemeHttp;
            return result;
        }
    }
}
