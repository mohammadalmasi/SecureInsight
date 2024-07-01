using SecureInsight.Repository;

namespace SecureInsight.APP
{
    public interface ICorpusService
    {
        void AddCorpus(Corpus item);
        IEnumerable<Corpus> GetAllCorpus();
    }

    public interface ILSTMMetricService
    {
        IEnumerable<LSTMMetric> GetLatestMetrics();
    }

    public interface IMLPMetricService
    {
        IEnumerable<MLPMetric> GetLatestMetrics();
    }

    public interface ICNNMetricService
    {
        IEnumerable<CNNMetric> GetLatestMetrics();
    }


}
