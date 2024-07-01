using Microsoft.Extensions.DependencyInjection;
using SecureInsight.APP;
using SecureInsight.Repository;
using System.Windows;

namespace SecureInsight.Wpf
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        public IServiceProvider? ServiceProvider { get; private set; }

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            var serviceCollection = new ServiceCollection();
            ConfigureServices(serviceCollection);

            ServiceProvider = serviceCollection.BuildServiceProvider();

            var mainWindow = ServiceProvider.GetRequiredService<MainWindow>();
            mainWindow.Show();
        }

        private void ConfigureServices(IServiceCollection services)
        {
            services.AddSingleton<DatabaseContext>(); // Assuming CorpusContext is registered as Singleton

            services.AddScoped<ICorpusRepository, CorpusRepository>();
            services.AddScoped<ILSTMMetricRepository, LSTMMetricRepository>();
            services.AddScoped<IMLPMetricRepository, MLPMetricRepository>();
            services.AddScoped<ICNNMetricRepository, CNNMetricRepository>();
            services.AddScoped<IUnitOfWork, UnitOfWork>();


            services.AddScoped<ICorpusService, CorpusService>();
            services.AddScoped<ILSTMMetricService, LSTMMetricService>();
            services.AddScoped<IMLPMetricService, MLPMetricService>();
            services.AddScoped<ICNNMetricService, CNNMetricService>();
            services.AddScoped<IFileMerger, FileMerger>();
            services.AddScoped<ITokenizer, Tokenizer>();

            

            // Register your main window if needed
            services.AddSingleton<MainWindow>();
        }
    }
}

