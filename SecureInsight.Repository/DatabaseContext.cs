using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Reflection.Emit;

namespace SecureInsight.Repository
{
    public class DatabaseContext : DbContext
    {
        public DbSet<Corpus> Corpus { get; set; }
        public DbSet<LSTMMetric> LSTMMetrics { get; set; }
        public DbSet<MLPMetric> MLPMetrics { get; set; }
        public DbSet<CNNMetric> CNNMetrics { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            var databasePath = @"C:\00\c#\SecureInsight.db";

            optionsBuilder.UseSqlite($"Data Source={databasePath}");
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Define any additional configurations for your model here
            modelBuilder.Entity<Corpus>()
                .HasKey(c => c.Id); // Set Id as the primary key
        }
    }
}
