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
    
    private function mb_substr_replace($string, $replacement, $start, $length=NULL) {
        if (is_array($string)) {
            $num = count($string);
            // $replacement
            $replacement = is_array($replacement) ? array_slice($replacement, 0, $num) : array_pad(array($replacement), $num, $replacement);
            // $start
            if (is_array($start)) {
                $start = array_slice($start, 0, $num);
                foreach ($start as $key => $value) {
                    $start[$key] = is_int($value) ? $value : 0;
                }
            }
            else {
                $start = array_pad(array($start), $num, $start);
            }
            // $length
            if (!isset($length)) {
                $length = array_fill(0, $num, 0);
            }
            elseif (is_array($length)) {
                $length = array_slice($length, 0, $num);
                foreach ($length as $key => $value) {
                    $length[$key] = isset($value) ? (is_int($value) ? $value : $num) : 0;
                }
            }
            else {
                $length = array_pad(array($length), $num, $length);
            }
            // Recursive call
            return array_map(__FUNCTION__, $string, $replacement, $start, $length);
        }
        preg_match_all('/./us', (string)$string, $smatches);
        preg_match_all('/./us', (string)$replacement, $rmatches);
        if ($length === NULL) $length = mb_strlen($string);
        array_splice($smatches[0], $start, $length, $rmatches[0]);
        return join($smatches[0]);
    }


    public function detectLanguage($string, $default_lang=null) {
        try {
            $ld = new Language;
            $ld_array = $ld->detect($string)->bestResults()->close();
            
            $detected_language_long = array_keys($ld_array)[0];
            $detected_language = mb_substr($detected_language_long, 0, 2);
        
            if((!array_key_exists($detected_language, $this->lang_to_code)) 
                    // TODO: check if we need this threshold
                    //|| sizeof($ld_array) > 1 && $ld_array[$detected_language_long] < 0.55
                    || sizeof($ld_array) > 3) {    
                $detected_language = null;
            }
        } catch (\Throwable $e) {
            error_log('Error detecting query language: ' . $e->getMessage());
            $detected_language = null;
            $ld_array = array("status" => "error");
        }
        
        return array(
            'detected_language' => $detected_language === null ? null : $detected_language
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
            if(isset($error->suggestions[0])) {
                $suggestion = mb_strtolower($error->suggestions[0]);
                $offset = intval($error->offset) + $additional_offset;
                $strlen = mb_strlen($error->word);
                
                if($suggestion !== mb_substr($new_string, $offset, $strlen)) {
                    $new_string = $this->mb_substr_replace($new_string
                            , $suggestion_prefix . $suggestion . $suggestion_postfix
                            , $offset
                            , $strlen);

                    $additional_offset += strlen($suggestion_prefix) + strlen($suggestion_postfix)
                                            + strlen($suggestion) - strlen($error->word);
                }
            }
        }
        
        return $new_string;
    }

    public function performSpellchecking($string, $verbose = false
            , $suggestion_prefix = '<span class="corrected-word">'
            , $suggestion_postfix = '</span>') {
        
        $new_string = "";
        $new_string_display = "";
        
        $ld = $this->detectLanguage($string);
        $lang = $ld['detected_language'];
        if($lang !== null) {
            $spelling_errors = $this->checkText($string, $this->lang_to_code[$lang]);

            if (!isset($spelling_errors["status"]) || $spelling_errors["status"] !== "error") {
                $new_string = $this->replaceWithSuggestion($string, $spelling_errors);
                $new_string_display = $this->replaceWithSuggestion($string, $spelling_errors
                        , $suggestion_prefix, $suggestion_postfix);
            }
        }
        
        $ret_array = array(
            'new_query' => $new_string
                , 'new_query_markup' => $new_string_display);
        
        if($verbose === true) {
            $ret_array["language_detection"] = $ld;
            if($lang !== null) {
                $ret_array["spellcheck"] = $spelling_errors;
            }
        }
        
        return $ret_array;
        
    }

}