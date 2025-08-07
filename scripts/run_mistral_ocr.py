#!/usr/bin/env python3
"""
Mistral OCR Script for Motia Invoice Processing Example

This script processes invoice images and PDFs using Mistral OCR and outputs
extracted text in a format suitable for Motia pipeline processing.
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import fitz  # PyMuPDF for PDF processing
from PIL import Image
import pytesseract

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MistralOCRProcessor:
    """Handles OCR processing using Mistral OCR (fallback to Tesseract)"""
    
    def __init__(self):
        """Initialize the OCR processor"""
        self.supported_formats = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.bmp']
        
        # Try to use Mistral OCR if available, otherwise fallback to Tesseract
        try:
            # This would be the actual Mistral OCR import when available
            # from mistral_ocr import OCR
            # self.ocr_engine = OCR()
            self.use_mistral = False
            logger.info("Using Tesseract OCR (Mistral OCR not available)")
        except ImportError:
            self.use_mistral = False
            logger.info("Using Tesseract OCR (Mistral OCR not available)")
    
    def validate_file(self, file_path: str) -> bool:
        """Validate if file is supported format"""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
            
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in self.supported_formats:
            logger.error(f"Unsupported format: {file_ext}")
            return False
            
        return True
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using Tesseract"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            return ""
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single file with OCR
        
        Args:
            file_path: Path to file to process
            
        Returns:
            Dictionary with OCR results
        """
        if not self.validate_file(file_path):
            return {
                "filename": os.path.basename(file_path),
                "success": False,
                "error": "Invalid file or unsupported format",
                "text": "",
                "file_type": Path(file_path).suffix.lower()
            }
        
        try:
            file_ext = Path(file_path).suffix.lower()
            
            logger.info(f"Processing: {file_path}")
            
            # Extract text based on file type
            if file_ext == '.pdf':
                text = self.extract_text_from_pdf(file_path)
            else:
                text = self.extract_text_from_image(file_path)
            
            if text:
                logger.info(f"OCR completed: {len(text)} characters extracted")
                return {
                    "filename": os.path.basename(file_path),
                    "success": True,
                    "text": text,
                    "file_type": file_ext,
                    "char_count": len(text)
                }
            else:
                logger.warning(f"No text extracted from {file_path}")
                return {
                    "filename": os.path.basename(file_path),
                    "success": False,
                    "error": "No text could be extracted",
                    "text": "",
                    "file_type": file_ext
                }
                
        except Exception as e:
            logger.error(f"OCR processing failed for {file_path}: {e}")
            return {
                "filename": os.path.basename(file_path),
                "success": False,
                "error": str(e),
                "text": "",
                "file_type": Path(file_path).suffix.lower()
            }
    
    def process_batch(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple files with OCR
        
        Args:
            file_paths: List of file paths to process
            
        Returns:
            List of OCR results
        """
        results = []
        
        for file_path in file_paths:
            result = self.process_file(file_path)
            results.append(result)
            
            # Output result for Motia to capture
            print(json.dumps(result))
        
        return results

def main():
    """Main entry point for the script"""
    if len(sys.argv) < 2:
        print("Usage: python run_mistral_ocr.py <file1> [file2] ...")
        sys.exit(1)
    
    # Get file paths from command line arguments
    file_paths = sys.argv[1:]
    
    # Initialize OCR processor
    processor = MistralOCRProcessor()
    
    # Process files
    results = processor.process_batch(file_paths)
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    
    logger.info(f"Processing complete: {successful}/{total} files successful")
    
    if successful == 0:
        sys.exit(1)

if __name__ == "__main__":
    main() 