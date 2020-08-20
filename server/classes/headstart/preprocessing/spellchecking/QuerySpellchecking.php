<?php

namespace headstart\preprocessing\spellchecking;

/**
 * Spellchecking for queries
 *
 * @author pkraker
 */
require_once 'Spellchecking.php';
@include __DIR__ . '../../../../vendor/autoload.php';

use LanguageDetection\Language;
use Mekras\Speller\Hunspell\Hunspell;
use Mekras\Speller\Source\StringSource;

class QuerySpellchecking extends Spellchecking {
    
    protected $lang_to_code;
    
    function __construct($ini_array) {
        parent::__construct($ini_array);
        $this->lang_to_code = $this->ini_array["lang_to_code"];
    }


    public function detectLanguage($string, $default_lang='en') {
        try {
            $ld = new Language;
            $ld_array = $ld->detect($string)->bestResults()->close();
            
            $detected_language = array_keys($ld_array)[0];
        
            if((sizeof($ld_array) > 1 && $ld_array[$detected_language] < 0.55) 
                    || !array_key_exists($detected_language, $this->lang_to_code)) {    
                $detected_language = $default_lang;
            }
        } catch (\Throwable $e) {
            error_log('Error detecting query language: ' . $e->getMessage());
            $detected_language = $default_lang;
            $ld_array = array("status" => "error");
        }
        
        return array(
            'detected_language' => $this->lang_to_code[$detected_language]
                , 'ld_array' => $ld_array
            );
        
    }
    
    public function checkText($string, $lang) {
        //TODO: find a better way to this
        putenv("LANG=$lang.UTF-8");
        $_SERVER['LANG'] = "$lang.UTF-8";
        
        try {
            $source = new StringSource($string);
            $speller = new Hunspell($this->ini_array["hunspell_path"]);
            $speller->setDictionaryPath($this->ini_array["dicts_path"]);
            $issues = $speller->checkText($source, [$lang, 'de']);
        } catch (\Throwable $e) {
            error_log('Error during spellcheck: ' . $e->getMessage());
            $issues = array("status"=>"error");
        }

        return $issues;
        
    }
    
    public function getQueryTermsArray($query) {

        //Replace terms within square brackets, as they denote fields in PubMed
        $query_wt_fields = preg_replace('/\[(.*?)\]/', '', $query);
        
         //Remove inverted commas, and, or, +, -, (, ) from query string 
        $query_wt_operators = preg_replace('/(^|\s)-|\+/', ' '
                            , preg_replace('/\band\b|\bor\b|\(|\)|\\"|\"/', '', $query_wt_fields));
        
        //Remove unnecessary white space
        $query_wt_whitespace = preg_replace('/\s+/', ' ', trim($query_wt_operators));
        
        //Merge term arrays and remove duplicate entries
        $term_array = array_unique(array_merge($term_array, explode(' ', $query_wt_whitespace)));

        return $term_array;
    }
    
    private function replaceWithSuggestion($string, $spelling_errors
            , $suggestion_prefix = "", $suggestion_postfix = "") {
        
        $new_string = $string;
        $additional_offset = 0;
        
        foreach($spelling_errors as $error) {
            $suggestion = $error->suggestions[0];
            
            $new_string = substr_replace($new_string
                    ,  $suggestion_prefix . $suggestion . $suggestion_postfix
                    , intval($error->offset) + $additional_offset
                    , strlen($error->word));
            
            $additional_offset += strlen($suggestion_prefix) + strlen($suggestion_postfix)
                                    + strlen($suggestion) - strlen($error->word);
        }
        
        return $new_string;
    }

    public function performSpellchecking($string, $verbose = false
            , $suggestion_prefix = '<span class="corrected-word">'
            , $suggestion_postfix = '</span>') {
        
        $ld = $this->detectLanguage($string);
        $lang = $ld['detected_language'];
        $spelling_errors = $this->checkText($string, $lang);
        
        $new_string = "";
        $new_string_display = "";
        
        if (!isset($spelling_errors["status"]) || $spelling_errors["status"] !== "error") {
            $new_string = $this->replaceWithSuggestion($string, $spelling_errors);
            $new_string_display = $this->replaceWithSuggestion($string, $spelling_errors
                    , $suggestion_prefix, $suggestion_postfix);
        }
        
        $ret_array = array(
            'new_query' => $new_string
                , 'new_query_markup' => $new_string_display);
        
        if($verbose === true) {
            $ret_array["language_detection"] = $ld;
            $ret_array["spellcheck"] = $spelling_errors;
        }
        
        return $ret_array;
        
    }

}