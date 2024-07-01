namespace SecureInsight.Repository
{
    public interface ICorpusRepository
    {
        IEnumerable<Corpus> GetAll();
        void Add(Corpus item);
    }

    public interface ILSTMMetricRepository
    {
        IEnumerable<LSTMMetric> GetLatestMetrics();
    }

    public interface IMLPMetricRepository
    {
        IEnumerable<MLPMetric> GetLatestMetrics();
    }

    public interface ICNNMetricRepository
    {
        IEnumerable<CNNMetric> GetLatestMetrics();
    }
}
