namespace SecureInsight.Repository
{
    public class CorpusRepository : ICorpusRepository
    {
        private readonly DatabaseContext _context;

        public CorpusRepository(DatabaseContext context)
        {
            _context = context;
        }

        public IEnumerable<Corpus> GetAll()
        {
            return _context.Corpus.ToList();
        }

        public void Add(Corpus item)
        {
            _context.Corpus.Add(item);
            _context.SaveChanges();
        }
    }

    public class LSTMMetricRepository : ILSTMMetricRepository
    {
        private readonly DatabaseContext _context;

        public LSTMMetricRepository(DatabaseContext context)
        {
            _context = context;
        }

        public IEnumerable<LSTMMetric> GetLatestMetrics()
        {
            var latestMetrics = _context.LSTMMetrics
                 .GroupBy(m => m.Mode)
                 .Select(g => g.OrderByDescending(m => m.ID).FirstOrDefault())
                 .ToList();

            return latestMetrics;
        }
    }

    public class MLPMetricRepository : IMLPMetricRepository
    {
        private readonly DatabaseContext _context;

        public MLPMetricRepository(DatabaseContext context)
        {
            _context = context;
        }

        public IEnumerable<MLPMetric> GetLatestMetrics()
        {
            var latestMetrics = _context.MLPMetrics
                 .GroupBy(m => m.Mode)
                 .Select(g => g.OrderByDescending(m => m.ID).FirstOrDefault())
                 .ToList();

            return latestMetrics;
        }
    }

    public class CNNMetricRepository : ICNNMetricRepository
    {
        private readonly DatabaseContext _context;

        public CNNMetricRepository(DatabaseContext context)
        {
            _context = context;
        }

        public IEnumerable<CNNMetric> GetLatestMetrics()
        {
            var latestMetrics = _context.CNNMetrics
                 .GroupBy(m => m.Mode)
                 .Select(g => g.OrderByDescending(m => m.ID).FirstOrDefault())
                 .ToList();

            return latestMetrics;
        }
    }
}
