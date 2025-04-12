Feature: Generate Certificate

  Scenario: A trainee completes a module
    Given I have completed all lessons in a module
    When I visit the module page
    Then I should see a downloadable certificate
