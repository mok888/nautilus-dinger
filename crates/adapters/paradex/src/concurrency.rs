// crates/adapters/paradex/src/concurrency.rs
//! Concurrency primitives for race condition protection

use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use tokio::sync::Semaphore;
use tokio::time::{Duration, Instant};

/// Atomic nonce generator for request ordering
#[derive(Debug, Clone)]
pub struct NonceManager {
    nonce: Arc<AtomicU64>,
}

impl NonceManager {
    pub fn new() -> Self {
        let start_nonce = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_millis() as u64;
        
        Self {
            nonce: Arc::new(AtomicU64::new(start_nonce)),
        }
    }
    
    /// Get next nonce atomically
    pub fn next(&self) -> u64 {
        self.nonce.fetch_add(1, Ordering::SeqCst)
    }
}

/// Rate limiter to prevent API throttling
#[derive(Debug, Clone)]
pub struct RateLimiter {
    semaphore: Arc<Semaphore>,
    max_per_second: usize,
}

impl RateLimiter {
    pub fn new(max_per_second: usize) -> Self {
        Self {
            semaphore: Arc::new(Semaphore::new(max_per_second)),
            max_per_second,
        }
    }
    
    /// Acquire permit, blocks if rate limit reached
    pub async fn acquire(&self) -> tokio::sync::SemaphorePermit<'_> {
        self.semaphore.acquire().await.unwrap()
    }
}

impl Drop for RateLimiter {
    fn drop(&mut self) {
        // Cleanup if needed
    }
}

/// Atomic order ID generator
#[derive(Debug, Clone)]
pub struct OrderIdGenerator {
    counter: Arc<AtomicU64>,
}

impl OrderIdGenerator {
    pub fn new() -> Self {
        Self {
            counter: Arc::new(AtomicU64::new(1)),
        }
    }
    
    /// Generate unique order ID
    pub fn next(&self) -> String {
        let id = self.counter.fetch_add(1, Ordering::SeqCst);
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_millis();
        format!("{}{:06}", timestamp, id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_nonce_uniqueness() {
        let manager = NonceManager::new();
        let n1 = manager.next();
        let n2 = manager.next();
        assert!(n2 > n1);
    }
    
    #[test]
    fn test_order_id_uniqueness() {
        let gen = OrderIdGenerator::new();
        let id1 = gen.next();
        let id2 = gen.next();
        assert_ne!(id1, id2);
    }
}
