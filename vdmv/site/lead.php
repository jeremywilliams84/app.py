<?php
header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  http_response_code(405);
  echo json_encode(['ok' => false, 'error' => 'Méthode non autorisée']);
  exit;
}
$name = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');
$source = trim($_POST['source'] ?? 'visible-dans-ma-ville');
$plan = trim($_POST['generated_plan'] ?? '');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
  http_response_code(400);
  echo json_encode(['ok' => false, 'error' => 'Email invalide']);
  exit;
}
$dir = __DIR__ . '/leads';
if (!is_dir($dir)) { mkdir($dir, 0755, true); }
$file = $dir . '/leads.csv';
$isNew = !file_exists($file);
$fp = fopen($file, 'a');
if (!$fp) {
  http_response_code(500);
  echo json_encode(['ok' => false, 'error' => 'Impossible d’enregistrer le lead']);
  exit;
}
if ($isNew) { fputcsv($fp, ['date', 'name', 'email', 'source', 'generated_plan'], ';'); }
fputcsv($fp, [date('c'), $name, $email, $source, $plan], ';');
fclose($fp);

// Optionnel : décommentez et remplacez l'adresse pour recevoir une notification email.
// $to = 'votre-email@exemple.com';
// $subject = 'Nouveau lead - Générateur métier + ville';
// $message = "Nom: $name\nEmail: $email\nSource: $source\n\nPlan:\n$plan";
// @mail($to, $subject, $message, "From: no-reply@" . ($_SERVER['HTTP_HOST'] ?? 'site.local'));

echo json_encode(['ok' => true]);
?>
