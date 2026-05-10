// based on https://github.com/huggingface/candle/blob/main/candle-transformers/src/generation/mod.rs

use crate::config::{SamplingParams, SAMPLING_EPS};
use rand::SeedableRng;

pub struct LogitsProcessor {
    pub rng: rand::rngs::StdRng,
    pub temperature: Option<f32>,
    pub top_p: f32,
}

impl LogitsProcessor {
    pub fn new(sampling_params: &SamplingParams) -> Self {
        let temperature = if sampling_params.temperature < SAMPLING_EPS {
            None
        } else {
            Some(sampling_params.temperature)
        };

        // Use deterministic seed for reproducible generation.
        // Default to 42 if no seed is specified.
        let seed = sampling_params.seed.unwrap_or(42);

        Self {
            rng: rand::rngs::StdRng::seed_from_u64(seed),
            temperature,
            top_p: sampling_params.top_p,
        }
    }

    pub fn set_temperature(&mut self, temperature: f32) {
        if temperature < SAMPLING_EPS {
            self.temperature = None;
        } else {
            self.temperature = Some(temperature);
        }
    }
}
