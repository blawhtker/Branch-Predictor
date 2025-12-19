import sys

class BranchPredictor:
    def __init__(self, m, n):
        self.m = m  # Number of PC bits (Table size = 2^M)
        self.n = n  # Number of GHR bits
        self.table_size = 1 << m
        
        # Initialize BHT (Branch History Table) with 2-bit counters.
        # "initialized to state 2 (Weakly taken)"
        self.bht = [2] * self.table_size
        
        # Initialize Global History Register (GHR) to 0
        self.ghr = 0

    # Calculates the index into the BHT.
    # Formula: XOR operation between the PC index and "Global History Record << (m-n)".
    # This aligns the GHR with the uppermost n bits of the PC index.
    def get_index(self, pc):
        
        # 1. Get the relevant M bits from the PC.
        # "The lowest two bits of the PC can be ignored"
        # We take M bits starting from bit 2.
        pc_index = (pc >> 2) & ((1 << self.m) - 1)
        
        # 2. Align GHR to the upper bits of the index mask
        ghr_shifted = self.ghr << (self.m - self.n)
        
        # 3. Perform XOR
        index = pc_index ^ ghr_shifted
        
        return index

    # Returns True if Taken, False if Not Taken.
    # Counter >= 2 predicts Taken.
    def predict(self, pc):

        index = self.get_index(pc)
        counter = self.bht[index]
        return counter >= 2

    # Updates the BHT counter and the GHR based on actual outcome.
    def update(self, pc, actual_taken):
        
        index = self.get_index(pc)
        
        # 1. Update the saturating counter
        # Saturation happens at 0 or 3.
        if actual_taken:
            if self.bht[index] < 3:
                self.bht[index] += 1
        else:
            if self.bht[index] > 0:
                self.bht[index] -= 1

        # 2. Update the Global History Register (GHR)
        # Assignment Requirement: "shifting the register to the right by one bit and 
        # placing the branch result into the position of the most-significant bit"
        if self.n > 0:
            outcome_bit = 1 if actual_taken else 0
            
            # Shift Right
            shifted_ghr = self.ghr >> 1
            
            # Insert at MSB (Position N-1)
            msb_mask = outcome_bit << (self.n - 1)
            
            self.ghr = msb_mask | shifted_ghr
        else:
            self.ghr = 0

# Main driver to parse the file and run predictions.
def run_simulation(trace_file, m, n):
    
    predictor = BranchPredictor(m, n)
    total_predictions = 0
    mispredictions = 0

    try:
        with open(trace_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) < 2:
                    continue
                
                pc_hex = parts[0]
                outcome_char = parts[1].lower()
                
                try:
                    pc = int(pc_hex, 16)
                except ValueError:
                    continue
                
                # "t" = taken, "n" = not taken
                actual_taken = (outcome_char == 't')
                
                # 1. Predict
                prediction = predictor.predict(pc)
                
                # 2. Check correctness 
                if prediction != actual_taken:
                    mispredictions += 1
                
                # 3. Update Predictor
                predictor.update(pc, actual_taken)
                
                total_predictions += 1
                
    except FileNotFoundError:
        print(f"Error: File {trace_file} not found.")
        return 0.0

    if total_predictions == 0:
        return 0.0

    return mispredictions / total_predictions

if __name__ == "__main__":
    
    # Expected format: ./sim gshare <GPB> <RB> <Trace_File>
    if len(sys.argv) == 5 and sys.argv[1] == 'gshare':
        try:
            m_arg = int(sys.argv[2])
            n_arg = int(sys.argv[3])
            trace_file_arg = sys.argv[4]
        except ValueError:
            print("Error: GPB and RB must be integers.")
            sys.exit(1)
            
        rate = run_simulation(trace_file_arg, m_arg, n_arg)
        
        # Output Format: <M> <N> <Misprediction Ratio>
        print(f"{m_arg} {n_arg} {rate:.4f}")
        
    else:
        print("Usage: ./sim gshare <GPB> <RB> <Trace_File>")
        sys.exit(1)