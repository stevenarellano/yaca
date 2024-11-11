# Few-shot examples for code performance

code_example_1 = """
performant code:    
void processLargeData(const std::vector<int>& data) {
    std::vector<int> processedData(data.size());
    for (size_t i = 0; i < data.size(); ++i) {
        processedData[i] = data[i] * 2;
    }
}

non-performant code:
void processLargeData(const std::vector<int>& data) {
    std::vector<int> processedData;
    for (size_t i = 0; i < data.size(); ++i) {
        processedData.push_back(data[i] * 2);
    }
}
"""

code_example_2 = """
performant code:
std::string generateLargeString() {
    std::string str = "This is a large string.";
    return str;
}

void useString() {
    std::string str = generateLargeString();
    // Use str
}

non-performant code:
std::string generateLargeString() {
    std::string str = "This is a large string.";
    return std::move(str); // Ineffective use of move; may create extra copies
}

void useString() {
    std::string str = generateLargeString();
    str = generateLargeString(); // Unnecessary copy operation
    // Use str
}
"""
