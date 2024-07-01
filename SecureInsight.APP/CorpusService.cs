using SecureInsight.Repository;

namespace SecureInsight.APP
{
    public class CorpusService : ICorpusService
    {
        private readonly IUnitOfWork _unitOfWork;

        public CorpusService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public void AddCorpus(Corpus item)
        {
            _unitOfWork.CorpusRepository.Add(item);
            _unitOfWork.Save();
        }

        public IEnumerable<Corpus> GetAllCorpus()
        {
            return _unitOfWork.CorpusRepository.GetAll();
        }
    }

    public class LSTMMetricService : ILSTMMetricService
    {
        private readonly IUnitOfWork _unitOfWork;

        public LSTMMetricService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public IEnumerable<LSTMMetric> GetLatestMetrics()
        {
            return _unitOfWork.LSTMMetricRepository.GetLatestMetrics();
        }
    }

    public class MLPMetricService : IMLPMetricService
    {
        private readonly IUnitOfWork _unitOfWork;

        public MLPMetricService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public IEnumerable<MLPMetric> GetLatestMetrics()
        {
            return _unitOfWork.MLPMetricRepository.GetLatestMetrics();
        }
    }

    public class CNNMetricService : ICNNMetricService
    {
        private readonly IUnitOfWork _unitOfWork;

        public CNNMetricService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public IEnumerable<CNNMetric> GetLatestMetrics()
        {
            return _unitOfWork.CNNMetricRepository.GetLatestMetrics();
        }
    }



}
