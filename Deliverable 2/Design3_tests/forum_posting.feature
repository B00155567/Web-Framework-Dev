Feature: Forum Posting

  Scenario: A trainee posts a question in the forum
    Given I am on the forum page for a module
    When I submit a question
    Then it should appear in the discussion thread
