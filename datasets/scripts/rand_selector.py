import random

def sentence_selector(file_path, n, min_word_count=10):
    """
    Selects n random lines from a file, ensuring that each line has at least min_word_count words.
    
    Args:
        file_path (str): Path to the input file.
        n (int): Number of lines to select.
        min_word_count (int): Minimum number of words required in each line.
        
    Returns:
        list: A list of selected lines.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if len(line.split()) >= min_word_count]
    
    return random.sample(lines, n) if len(lines) >= n else lines
    