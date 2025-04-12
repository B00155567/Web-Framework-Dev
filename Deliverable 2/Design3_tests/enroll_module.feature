Feature: Enroll in a Training Module

  Scenario: A trainee enrolls in an available module
    Given I am logged in as a trainee
    When I view the list of available modules
    And I click "Enroll" on a module
    Then I should see the module added to my enrolled list
