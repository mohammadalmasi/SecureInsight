namespace SecureInsight.Repository
{
    public class BaseMmetric
    {
        public int ID { get; set; }
        public string Mode { get; set; }
        public float Accuracy { get; set; }
        public float Precision { get; set; }
        public float Recall { get; set; }
        public float F1_Score { get; set; }
    }

    public class LSTMMetric : BaseMmetric
    {

    }

    public class MLPMetric : BaseMmetric
    {

    }

    public class CNNMetric : BaseMmetric
    {

    }
}
