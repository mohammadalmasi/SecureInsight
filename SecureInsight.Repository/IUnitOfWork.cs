namespace SecureInsight.Repository
{
    public interface IUnitOfWork : IDisposable
    {
        ICorpusRepository CorpusRepository { get; }
        ILSTMMetricRepository LSTMMetricRepository { get; }
        IMLPMetricRepository MLPMetricRepository { get; }
        ICNNMetricRepository CNNMetricRepository { get; }

        void Save();
    }

    public class UnitOfWork : IUnitOfWork
    {
        private readonly DatabaseContext _context;
        public ICorpusRepository CorpusRepository { get; private set; }
        public ILSTMMetricRepository LSTMMetricRepository { get; set; }
        public IMLPMetricRepository MLPMetricRepository { get; set; }
        public ICNNMetricRepository CNNMetricRepository { get; set; }

        public UnitOfWork(DatabaseContext context)
        {
            _context = context;
            CorpusRepository = new CorpusRepository(_context);
            LSTMMetricRepository = new LSTMMetricRepository(_context);
            MLPMetricRepository = new MLPMetricRepository(_context);
            CNNMetricRepository = new CNNMetricRepository(_context);
        }

        public void Save()
        {
            _context.SaveChanges();
        }

        public void Dispose()
        {
            _context.Dispose();
        }
    }

}
